# ADR-11 Snapshot
```
Status:
Created: 2018-10-09
Accepted:
```

## Context

Currently, to start a full node it requires to download the whole chain.
At the time of writing, Bitcoin's chain weights 200GB, and they generate
the block every 10 minutes. In our case, we create the block every 15 seconds
which will lead to significantly larger chain size. Besides consuming
a lot of space and a long time to sync the node, downloading the whole chain
causes also high bandwidth usage. According to [statoshi.info](https://statoshi.info/dashboard/db/bandwidth-usage?panelId=6&fullscreen),
on average `block` message consumes 252 KB/s of outbound traffic which is
~12x more than the second `tx` message, 20 KB/s. The reason is that many nodes
are being added to the network but have a short lifetime. We can see this pattern on
[bitnodes](https://bitnodes.earn.com/nodes/network-map/)

## Decision

To reduce bandwidth, storage and time to sync, we should introduce the snapshot
which is the set of UTXOs. Effectively, to validate/propose new transactions/blocks
the node needs to know only UTXOs.

### Snapshot schema (on the disk)

Snapshot is the collection of UTXOSubset. The schema of one UTXOSubset is the following:

**UTXOSubset**

field | type | bytes | description
--- | --- | --- | ---
txId | uint256 | 32 | TX hash
height | uint32 | 4 | block height the TX was included
isCoinBase | bool | 1 | set if it's a coinBase TX
output count | VarInt | 1-9 | number of outputs this TX contains
index | uint32 | 4 | output index
output | CTxOut | | the actual output

The reason of introducing `UTXOSubset` instead of using `Coin` class is to
reduce the storage as we don't need to serialize `outPoint`, `height` and `isCoinBase`
for every output.

**CTxOut**

field | type | bytes | description
--- | --- | --- | ---
CAmount | int64 | 8 | amount the output has
script size | VarInt | 1-9 | size of the script data
script data | vector\<unsigned char> | | script data

To calculate the snapshot hash, we use `ECMH(UTXO)` (details about ECMH see AD-10).
The reason we introduce `UTXO` instead of using `UTXOSubset` for computing the hash
is that `UTXO` represents one output. It means that we can add/subtract outputs even
without looking into the disk. The reason of not using the `Coin` class is that
it doesn't use the standard network serialization.

Scheme of **UTXO**

field | type | bytes | description
--- | --- | --- | ---
outPoint | COutPoint | 36 | pointer to the output it spends
height | uint32 | 4 | block height the TX was included
isCoinBase | bool | 1 | set if it's a coinBase TX
output | CTxOut | | the actual output

**COutPoint**

field | type | bytes | description
--- | --- | --- | ---
hash | uint256 | 32 | tx hash
n | uint32 | 4 | index of the output

Reasons of picking these fields and their types to compute the hash:
1. `outPoint` is the identifier of the output by which the `Coin` in levelDB is found.
2. `height`, `isCoinBase` and `output` are used because after downloading the
snapshot, there is no way to check that the following fields were part of the tx hash.
3. `height` is 32 bits instead of 31 bit (as in the `Coin`) is it's how the height
is serialized in the `version` P2P message.
4. `isCoinBase` has 1 byte instead of being part of the height (as in the `Coin`) is
that it allows us to introduce other TX types in the future without breaking the protocol.

Sample code of computing the snapshot hash:
```c++
secp256k1_context *ctx = secp256k1_context_create(SECP256K1_CONTEXT_NONE);
secp256k1_multiset multiset;
secp256k1_multiset_init(ctx, &multiset);

secp256k1_multiset_add(ctx, &multiset, utxo_0.data(), utxo_0.size());
secp256k1_multiset_add(ctx, &multiset, utxo_1.data(), utxo_1.size());
secp256k1_multiset_add(ctx, &multiset, utxo_2.data(), utxo_2.size());

uint256 hash;
secp256k1_multiset_finalize(ctx, in.data(), &multiset);
return hash;
```
Notice: there is no count byte in front of the message.

### Snapshot generation

Ideally, we would like to compute the snapshot for every block the node sees. However, computation
of the snapshot is expensive. It takes roughly 20 minutes to dump all the UTXO sets from the chainstate DB
and compute the ECMH of it. To overcome this, we will generate the snapshot only for the checkpoint
that can be potentially finalized epoch with the step of `150` epochs. The reason of doing it every 150 epochs is
to generate the snapshot ~1/day. Current block rate is: `1 block/15 secs or 1/15*60*60*24 = 5760 blocks = 115 epochs`

Once the node receives the block which has `height % 150 == 0`, after processing the block (and making it the tip),
node takes the levelDB snapshot (iterator of `chainstate`) and tries to generate the actual snapshot in the separate
thread. Taking the levelDB iterator, it guarantees that we have the same view of `chainstate` while we are keeping it.

If the snapshot was successfully generated, we store its ID in `chainstate` DB for later retrieval. The node should keep
last `5` snapshots. Validators always create snapshots. Proposers can disable snapshot creation by starting the node with flag `-createsnapshot=0`.

### Snapshot verification

To guarantee that the snapshot is a valid one and other nodes can trust it, we add the snapshot hash to the chain.
Every proposer must include the snapshot hash inside the CoinBase transaction as part of the script of the first input.
The schema of the input is the following:
```
CTxIn(
    scriptSig = CScript() << CScriptNum::serialize(nHeight) << snapshotHash << OP_0;
)
```
The reason to use input instead of output is to not add this hash to the chainstate and making it larger.

Everyone who receives the block must validate that it has the correct snapshot hash.
Snapshot hash points to the UTXOs of all blocks until the current one.
To visualize it:

```
H - height
S - snapshot

H=0 (S=null)
*-----
blocks

* genesis block points to the empty snapshot hash


H=0        H=1 (S=0)
*----------*-------
snapshot 0 | blocks

* at hight 1 coinbase TX points to the snapshot that has only genesis UTXOs


H=0        H=1 (S=0)   H=2 (S=1)
*----------*-----------*---
snapshot 1             | blocks

* at height 2 coinbase TX points to the snapshot that has UTXOs from H=0 and H=1

```

### Initial Snapshot Download (ISD)

To start the node in ISD mode, it's required to set two parameters:

1. `-prune=n` (n >= 1)
2. `-isd=1`
If pruning mode is not enabled, the regular IBD will be used. This ADR proposes to make ISD as an extension to the pruning.
Later we might revise it and make ISD enabled by default. 

Once the node is started in `-isd=1` mode, it will perform the following:

1. node downloads all the headers
2. node sends the initial `getsnapshot` message to its peers
3. when the first `snapshot` chunk is received, node verifies that `bestBlockHash` is part of the known headers
4. node keeps requesting remaining `snapshot` chunks
5. if one of the peers replied with the `snapshot` chunk that points to the higher block, the node will switch to it
6. when the final `snapshot` chunk is downloaded, node verifies the hash of the whole snapshot
7. if snapshot hash is incorrect, node bans the peer and restarts the process from step 2
8. when the last chunk is downloaded node verifies its hash.
9. if the hash is invalid, the node bans the peer and restarts the process from step 2
10. node requests the block which is the parent block of the snapshot
11. if parent block doesn't contains the hash of the snapshot node bans the peer and restarts the process from step 2.
12. node applies the snapshot and leaves ISD

### P2P messages

There are two new P2P messages:

1. `getsnapshot` to request the snapshot
2. `snapshot` to reply with the snapshot chunk

**getsnapshot**

field | type | bytes | description
---   | --- | --- | ---
bestBlockHash  | uint256 | 32 | at which block the snapshot is created
utxoSubsetIndex | uint64 | 8 | index of the first UTXO subset in the snapshot
utxoSubsetCount | uint16 | 2 | number of UTXO subsets to return

During the initial request:
* _bestBlockHash_ must be empty
* _utxoSubsetIndex_ set to 0
* _utxoSubsetCount_ any number larger than 0

After the first chunk of data is received, message should have the following values:
* _bestBlockHash_ is set according to the response in _snapshot_ message
* _utxoSubsetIndex_ is the next starting index to request. `utxoSubsetIndex = snapshot.utxoSubsetIndex + snapshot.utxoSubsetCount`
* _utxoSubsetCount_ any number larger than 0

**snapshot**

field | type | bytes | description
---   | --- | --- | ---
snapshotHash  | uint256 | 32 | ECMH of all UTXOs
bestBlockHash  | uint256 | 32 | at which block the snapshot is created
totalUTXOSubsets | uint64 | 8 | number of all UTXO subsets in the snapshot
utxoSubsetIndex | uint64 | 8 | index of the first UTXO subset in the snapshot
utxoSubsetCount | VarInt | 1-9 | number of UTXO subsets in the message
utxoSubsets | []UTXOSubset | | actual UTXO subsets and their outputs

Once the `snapshot` message has the condition `totalUTXOSubsets = utxoSubsetIndex + utxoSubsetCount`
it is considered the last chunk and no more `getsnapshot` messages should be requested.

## Consequences

1. snapshot hash becomes part of the consensus rule. Everyone needs to perform extra work to compute the hash
2. block size increases by 32 bytes as we add snapshot hash to the script of coinbase input
3. every node that generates the snapshot, has extra work (~20 min to produce the snapshot on the current bitcoin UTXOs)
4. extra disk space usage for full nodes, as they keep the whole chain + 5 snapshots.
