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

Snapshot is the collection of UTXOSets. The schema of one UTXOSet is the following:

**UTXOSet**

field | type | bytes | description
--- | --- | --- | ---
txId | uint256 | 32 | TX hash
height | uint32 | 4 | block height the TX was included
isCoinBase | bool | 1 | set if it's a coinBase TX
output count | VarInt | 1-9 | number of outputs this TX contains
index | uint32 | 4 | output index
output | CTxOut | | the actual output

To calculate the snapshot hash, we concatenate all UTXO sets and compute `SHA256`.
Sample code:
```c++
CSHA256 sha256;
sha256.Write(utxo_set_0, utxo_set_0_size);
sha256.Write(utxo_set_1, utxo_set_1_size);
sha256.Write(utxo_set_n, utxo_set_n_size);

uint256 hash;
sha256.Finalize(hash.begin());
return hash;
```
Notice: there is no count byte in front of the message.

### Snapshot generation

Ideally, we would like to compute the snapshot for every block the node sees. However, computation
of the snapshot is expensive. It takes roughly 10 minutes to dump all the UTXO sets from the chainstate DB
and compute the SHA256 hash of it. To overcome this, we will generate the snapshot only for the checkpoint
that can be potentially finalized epoch with the step of `150` epochs. The reason of doing it every 150 epochs is
to generate the snapshot ~1/day. Current block rate is: `1 block/15 secs or 1/15*60*60*24 = 5760 blocks = 115 epochs`

Once the node receives the block which has `height % 150 == 0`, after processing the block (and making it the tip),
node takes the levelDB snapshot (iterator of `chainstate`) and tries to generate the actual snapshot in the separate
thread. Taking the levelDB iterator, it guarantees that we have the same view of `chainstate` while we are keeping it.

If the snapshot was successfully generated, we store its ID in `chainstate` DB for later retrieval. The node should keep
last `5` successfully verified snapshots. (Verification is explained in the next section). Validators always
create snapshots. Proposers can disable snapshot creation by starting the node with flag `-createsnapshot=0`.

### Snapshot verification

To guarantee that the snapshot is a valid one and other nodes can trust it, we add the snapshot hash to the chain.
Only `validators` can add the snapshot hash to the chain. Snapshot hash is inside 2nd output of the `Vote` TX.
The schema of the output is the following:
```
CTxOut(
    nValue = 0,
    scriptPubKey = OP_RETURN << snapshotHash
)
```

Including the snapshot hash is _optional_ and validators should include it only every `150` epochs and this snapshot
should point to the block height which is `150` epochs ago. The following graph visualizes it:

```
H - height
E - epoch
S - snapshot

       E=149 (S=null)
-------*-------
blocks | blocks

* at this stage there is no snapshot in the chain


       E=150 (S=null)
-------*-------
blocks | blocks

* at hight 7500 validators start generating the first snapshot


           E=150                    E=300            E=301
           H=7500   H=7501  .....   H=15000 S=0      H=15050
-----------*--------*---------------*----------------*
snapshot 0          | blocks

* validators voted for E=300 and included the snapshot hash which points to E=150
* snapshot 0 contains UTXO sets until height 7500 (including).


           E=150        E=300                        E=450             E=451
           H=7500 S=0   H=15000 S=0     H=15001      H=22500 S=1       H=22550
-----------*------------*---------------*------------*-----------------*
snapshot 1                              | blocks

* validators voted for E=450 and included the snapshot hash which points to E=300
* snapshot 1 contains UTXO sets until height 15000 (including).

```

Snapshot hash is considered valid if 2/3 of votes have the same hash

If consensus for the snapshot hash is not reached, nodes that generated such snapshot can delete it.
Snapshot hash is _optional_ because a validator that started generating it might be not on a fork which
eventually became finalized. This ADR doesn't propose any penalty for producing incorrect snapshot hash.

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
10. node requests blocks which should contain votes for the downloaded snapshot
11. if there are no 2/3 of votes for the downloaded snapshot node bans the peer and restarts the process from step 2.
12. node applies the snapshot and leaves ISD

### P2P messages

There are two new P2P messages:

1. `getsnapshot` to request the snapshot
2. `snapshot` to reply with the snapshot chunk

**getsnapshot**

field | type | bytes | description
---   | --- | --- | ---
bestBlockHash  | uint256 | 32 | at which block the snapshot is created
utxoSetIndex | uint64 | 8 | index of the first UTXO set in the snapshot
utxoSetCount | uint16 | 2 | number of UTXO sets to return

During the initial request:
* _bestBlockHash_ must be empty
* _utxoSetIndex_ set to 0
* _utxoSetCount_ any number larger than 0

After the first chunk of data is received, message should have the following values:
* _bestBlockHash_ is set according to the response in _snapshot_ message
* _utxoSetIndex_ is the next starting index to request. `utxoSetIndex = snapshot.utxoSetIndex + snapshot.utxoSetCount`
* _utxoSetCount_ any number larger than 0

**snapshot**

field | type | bytes | description
---   | --- | --- | ---
snapshotHash  | uint256 | 32 | SHA256 of all UTXO sets
bestBlockHash  | uint256 | 32 | at which block the snapshot is created
totalUTXOSets | uint64 | 8 | number of all UTXO sets in the snapshot
utxoSetIndex | uint64 | 8 | index of the first UTXO set in the snapshot
utxoSetCount | VarInt | 1-9 | number of UTXO sets in the message
utxoSets | []UTXOSet | | actual UTXO sets and their outputs

Once the `snapshot` message has the condition `totalUTXOSets = utxoSetIndex + utxoSetCount`
it is considered the last chunk and no more `getsnapshot` messages should be requested.

## Consequences

1. every node that generates the snapshot, has extra work (10 min to produce the snapshot)
2. extra disk space usage for full nodes, as they keep the whole chain + 5 snapshots
3. vote transactions which contain the snapshot hash have one additional output
