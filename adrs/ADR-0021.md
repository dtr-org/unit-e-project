# ADR-21 Transfer Esperanza Transactions

```
Status:   Draft
Created:  2018-11-08
Accepted:
```

This ADR is obsoleted by [ADR-23](ADR-23.md)

## Context

We're implementing a Casper-inspired finalization protocol named Esperanza. As
part of the protocol we need to adapt [fork choice rule](ADR-12.md), a
significant portion of that change is to follow the longest justified chain. To
represent justification and finalization, we have the finalization state for
every chain which is based on transactions of blocks that belong to the chain.

To explain the problem imagine Node A has the longest chain and Node B has the
shortest but recently justified one. Nodes were disconnected/unsynced, so were
able to build different chains, and eventually get connected to each other.


```
main finalized root
     ∨
     R ... - A1 - A2 - A3 - A4 - A5   Node A
     ------------------------------
           \ B1 - B2 - B3             Node B
                  ^
               justified
```

According to the fork-choice rule, after being connected Node A must switch to
longest justified chain with tip B3. To calculate B3's finalization state Node A
needs Esperanza transactions for blocks B1, B2, and B3. The current p2p
implementation which is taken from bitcoin prohibits this as it won't download
B1, B2, and B3 blocks since their tip's Work is less than the work of A5.

So we need a way to take Esperanza transactions from B1, B2, and B3. The
significant bound is that we won't take transactions from blocks from previous
dynasties (i.e., which height is below last finalization point).

Esperanza transactions are:

* DEPOSIT
* VOTE
* LOGOUT
* SLASH
* WITHDRAW
* ADMIN

## Decision

We extract Esperanza transactions (which we'd name Commits below) from the
block's transaction section to independent section. We remove commits from
transactions' Merkle root calculation. We add new Merkle root for
commits.

### Global chain state

Bitcoin's global chain state is built around:

```
map<uint256, CBlockIndex*> mabBlockIndex; // block hash -> CBlockIndex
CChain chainActive;
```

Where:

* CBlockIndex is a data structure built after process the CBlockHeader.
* CChain contains a sequence of these CBlockIndex-es starting from the genesis.

### Data types

```
CBlockHeader:
    int32_t nVersion;
    uint256 hashPrevBlock;
    uint256 hashMerkleRoot; // change: no commits in this merkle tree
    uint256 hashWitnessMerkleRoot // change: no commits in this merkle tree
    unit256 hashMerkleRootCommits; // addition
    uint32_t nTime;
    uint32_t nBits;

CBlockCommits: CBlockHeader // addition
    tx_t vCommits[];        // addition

CBlock: CBlockCommits       // change
    tx_t txns[];            // change: no commits in txns

CBlockIndex:
    ...
    tx_t vCommits[];        // addition
```

### P2P

After the node gets to know about block's header (`headers` or `cmpctblock`),
and if it has no commits for this block, it asks them from the peer using
`getblockcommits` and marks this request as in-flight.

#### Header (change)

The header type, which is encoded in the `headers` and `cmpctblocks` messages.

```
4     version
32    prev_block
32    merkle_root           -- change: no commits in merkle_root
32    witness_merkle_root   -- change: no commits in witness_merkle_root
32    merkle_root_commits   -- addition
4     timestamp
4     bits
```

#### getblockcommits (new)

Request commits for the `block_hash`. After peer received this message, it must
response with `blockcommits`.

```
32   block_hash
```

#### blockcommits (new)

Send this message in response to `getblockcommits`.

```
32    block_hash
 ?    commits_count         -- note: varint
 ?    commits
```

#### block (change)

```
4     version
32    prev_block
32    merkle_root           -- change: no commits in merkle_root
32    witness_merkle_root   -- change: no commits in witness_merkle_root
32    merke_root_commits    -- addition
4     timestamp
4     bits
 ?    commits_count         -- addition (varint)
 ?    commits               -- addition
 ?    txn_count             -- change: no commits in txn_count (varint)
 ?    txns                  -- change: no commits in txns
```

### Significant code places to implement or adjust

* Commits exchange;
* Header, block, and compact block handlers;
* Block header hash function;
* Commits Merkle root;
* Constructing finalization state from commits;
* Filling commits and transactions from the mempool;
* Header and block serialization and deserialization;
* A lot of unit and functional tests.

### Constructing finalization state

The only change here is to adjust the Esperanza interface in order to process
transactions came from commits instead of the whole block. It's going to be
changed more significantly as part of [ADR-12](ADR-12.md) implementation.

### Esperanza validation

Esperanza validation requires access to the previous Esperanza transactions
given from the mempool if any, or read block from the disk and see in
transaction section. This must be adjusted to take such transactions from
commits part of the CBlockCommits.

### Usual block sync

This ADR adds additional round-trip for headers exchange.

* When a node receives header, if it doesn't have corresponding commits, send
  `getblockcommits` message;
* Don't send `getdata(blocks)` and `getblockcommits` at the same time: it
  adds unnecessary round-trip because `block` already contains commits.
* When a node receives `blockcommits` or `block` message, update commits state.
* Once a node has commits in the correct order it can update finalization state.

#### Legacy Relaying

Block is from the last dynasty and *not a part* of the main chain.
```
        Node A               Node B
 -block-> |                    |
          | -----headers-----> |
          | <-getblockcommits- |
          | ---blockcommits--> |
```
Block is from the last dynasty and *a part* of the main chain.

```
        Node A               Node B
 -block-> |                    |
          | -----headers-----> |
          | <----getdata------ |
          | ------block------> |
```

#### High Bandwidth Relaying

Block is from the last dynasty and *not a part* of the main chain.

```
        Node A               Node B
          | <--sendcmpct(1)--- |
 -block-> |                    |
          | ----cmpctblock---> |
          | <-getblockcommits- |
          | ---blockcommits--> |
```

Block is from the last dynasty and *a part* of the main chain.
```
        Node A               Node B
          | <--sendcmpct(1)--- |
 -block-> |                    |
          | ----cmpctblock---> |
          | <-getblockcommits- |
          | ---blockcommits--> |
          | <---getblocktxn--- |
          | -----blocktxn----> |
```

#### Low Bandwidth Relaying

Block is from the last dynasty and *not a part* of the main chain.

```
        Node A               Node B
          | <--sendcmpct(0)--- |
 -block-> |                    |
          | -----headers-----> |
          | ----cmpctblock---> |
          | <-getdata(CMPCT)-- |
          | ----cmpctblock---> |
          | <-getblockcommits- |
          | ---blockcommits--> |
```

Block is from the last dynasty and *a part* of the main chain.
```
        Node A               Node B
          | <--sendcmpct(0)--- |
 -block-> |                    |
          | -----headers-----> |
          | ----cmpctblock---> |
          | <-getdata(CMPCT)-- |
          | ----cmpctblock---> |
          | <-getblockcommits- |
          | ---blockcommits--> |
          | <---getblocktxn--- |
          | -----blocktxn----> |
```

### Fast sync

Right now fast sync implementation ignores Esperanza transactions and it's a
subject of additional research/ADR, but at first sight, this ADR could
significantly simplify further work on this area. At the first step of the fast
sync, node downloads all headers of the current chain. After receiving of the
headers, node will follow to the general commits exchange algorithm and finally
obtain the correct finalization state. Further, it might be optimized even more so
that node will receive header with commits as a single message.

### SPV

As an initial syncing process is downloading of block headers, SPV can follow
usual headers exchange protocol and obtain commits so that it can restore
finalization state. Further, it might be optimized in the same way as fast sync.

## Consequences

We will extract commits from the main block's transactions and send them within
additional round-trip.

## Comments

1. Further, the protocol might be optimized for sync and spv cases, so commits could
be sent within headers during the sync.
