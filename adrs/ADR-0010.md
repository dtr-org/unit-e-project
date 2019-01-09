# ADR-10 Snapshot Verification

```
Status:   Accepted
Created:  2018-10-04
Accepted: 2018-12-31
```

## Context

### Initial Snapshot Download

When spawning a new node it downloads the blockchain and verifies it, before it starts
properly participating in the network. This is necessary to identify double spends and
what unspent transaction outputs there are which can be spent.

This takes a considerable amount of bandwidth, time to sync, and computing power to
verify. In order to have nodes join the network more quickly a fast sync mechanism would
be beneficial.

Bitcoin already supports pruning mode in which it downloads only part of the blockchain
and iterates through the blockchain in a sliding window manner, such that at any given
time it does not require more then a certain amount if disk space. It still downloads the
full blockchain and scans through it, thus it only saves disk space, not bandwidth or
computing power.

In order to determine what balance a wallet has only the _unspent transaction outputs_
(UTXOs) are needed (that is the spendable money in the system). The idea behind the
_initial snapshot download_ (ISD) is to simply download the set of UTXOs only instead
of the whole blockchain. The UTXO set can be used to determine the spendable funds
and a node can start staking (proposing or validating right away).

### Requirements

- Calculating and providing a snapshot should be an optional feature, that is it should
  be possible to spawn a node with ISD support activated or deactivated. P2P nodes use
  version bits for feature negotiation.
- Ideally no additional consesus rules should be neeed to be added to the system.
- The liveness of the system should not be affected by the fast sync / ISD mechanism,
  that is: Even if a majority of the nodes do not activate ISD the network should still
  function.

### Security concerns

A node downloading a snapshot can not know whether this snapshot is legitimate or not.
Thus the network needs to provide a simple way of verifying a downloaded snapshot (for
example a hash of a snapshot at given block height). The downloaded snapshot could then
be verified by computing its hash and comparing it to the known hash value from the
network. This value unfortunately is another critical value just like the block hash
of the tip of the active chain, thus posing another consensus aspect.

The problem is complicated by the fact that the feature is optional. Thus not every node
can deliver this information. Malicious nodes could take over, the less nodes having ISD
activated, the easier; providing false snapshots to newly spawned ISD nodes.

## Proposal: Rolling Hash using ECMH

In order to provide the hash of a snapshot for a given block height this proposal
suggests to include the UTXO set hash in the coinbase transaction of every block
(alternatively, if this is considered too costly, every k-th block, where k might
be the epoch size with regards to finalization or the frequency of snapshot
generation with respect to the current implementation).

Since the feature is optional not every node should have to keep a snapshot
available. The computation of the UTXO set hash must be cheap to compute. Thus
this proposal suggests to calculate the UTXO set hash incrementally.

Example:

```
    BLOCK       TRANSACTIONS      SPENT    CREATED      UTXO SET
    -----       ------------      -----    -------      --------
in:
    Block-0
out:            u0 u1                                   {u0, u1}
                                                        
in:               u0              {u0}
    Block-1      /  \  
out:            u2  u3                     {u2, u3}     

                                                        {u1, u2, u3}
```

In this tiny example `Block-0` created two outputs _u0_ and _u1_ which makes
the UTXO set at height `0` be `{u0, u1}`. `u0` is then spent at height `1`
and creates two new outputs `u2` and `u3`.

In order to compute the UTXO set hash at height `1` a node can either
compute the hash of the complete UTXO set or it can build the hash incrementally
from the known UTXO set hash at height `0`. This requires the hash function
to support the deletion of a hash from it. With a large UTXO set this computation
should be dramatically cheaper then hashing the whole UTXO set. Also it requires
only looking at the in/outs of a single block.

We considered several functions for hashing/checksumming the UTXO set that exhibit
that property:

- XOR
- MuHash
- ECMH (Elliptic Curve Multiset Hashing, not to be confused with ECOH)

XOR is vulnerable as a snapshot can easily be tempered with by finding a subset
that xor's to zero (and can be removed then without altering the snapshots hash).

These options are also discussed in a discussion on the bitcoin-dev mailing list:

> ### 1. Incremental hashing
> 
> Computing a hash of the UTXO set is easy when it does not need
> efficient updates, and when we can assume a fixed serialization with a
> normative ordering for the data in it - just serialize the whole thing
> and hash it. As different software or releases may use different
> database models for the UTXO set, a solution that is order-independent
> would seem preferable.
> 
> This brings us to the problem of computing a hash of unordered data.
> Several approaches that accomplish this through incremental hashing
> were suggested in [5], including XHASH, AdHash, and MuHash. XHASH
> consists of first hashing all the set elements independently, and
> XORing all those hashes together. This is insecure, as Gaussian
> elimination can easily find a subset of random hashes that XOR to a
> given value. AdHash/MuHash are similar, except addition/multiplication
> modulo a large prime are used instead of XOR. Wagner [6] showed that
> attacking XHASH or AdHash is an instance of a generalized birthday
> problem (called the k-sum problem in his paper, with unrestricted k),
> and gives a O(2^(2*sqrt(n)-1)) algorithm to attack it (for n-bit
> hashes). As a result, AdHash with 256-bit hashes only has 31 bits of
> security.
> 
> Thankfully, [6] also shows that the k-sum problem cannot be
> efficiently solved in groups in which the discrete logarithm problem
> is hard, as an efficient k-sum solver can be used to compute discrete
> logarithms. As a result, MuHash modulo a sufficiently large safe prime
> is provably secure under the DL assumption. Common guidelines on
> security parameters [7] say that 3072-bit DL has about 128 bits of
> security. A final 256-bit hash can be applied to the 3072-bit result
> without loss of security to reduce the final size.
> 
> An alternative to multiplication modulo a prime is using an elliptic
> curve group. Due to the ECDLP assumption, which the security of
> Bitcoin signatures already relies on, this also results in security
> against k-sum solving. This approach is used in the Elliptic Curve
> Multiset Hash (ECMH) in [8]. For this to work, we must "hash onto a
> curve point" in a way that results in points without known discrete
> logarithm. The paper suggests using (controversial) binary elliptic
> curves to make that operation efficient. If we only consider
> secp256k1, one approach is just reading potential X coordinates from a
> PRNG until one is found that has a corresponding Y coordinate
> according to the curve equation. On average, 2 iterations are needed.
> A constant time algorithm to hash onto the curve exists as well [9],
> but it is only slightly faster and is much more complicated to
> implement.
> 
> AdHash-like constructions with a sufficiently large intermediate hash
> can be made secure against Wagner's algorithm, as suggested in [10].
> 4160-bit hashes would be needed for 128 bits of security. When
> repetition is allowed, [8] gives a stronger attack against AdHash,
> suggesting that as much as 400000 bits are needed. While repetition is
> not directly an issue for our use case, it would be nice if
> verification software would not be required to check for duplicated
> entries.
> 
> ### 2. Efficient addition and deletion
> 
> Interestingly, both ECMH and MuHash not only support adding set
> elements in any order but also deleting in any order. As a result, we
> can simply maintain a running sum for the UTXO set as a whole, and
> add/subtract when creating/spending an output in it. In the case of
> MuHash it is slightly more complicated, as computing an inverse is
> relatively expensive. This can be solved by representing the running
> value as a fraction, and multiplying created elements into the
> numerator and spent elements into the denominator. Only when the final
> hash is desired, a single modular inverse and multiplication is needed
> to combine the two.
> 
> As the update operations are also associative, H(a)+H(b)+H(c)+H(d) can
> in fact be computed as (H(a)+H(b)) + (H(c)+H(d)). This implies that
> all of this is perfectly parallellizable: each thread can process an
> arbitrary subset of the update operations, allowing them to be
> efficiently combined later.
> 
> ### 3. Comparison of approaches
> 
> Numbers below are based on preliminary benchmarks on a single thread
> of a i7-6820HQ CPU running at 3.4GHz.
> 
> 1. (MuHash) Multiplying 3072-bit hashes mod 2^3072 - 1103717 (the
> largest 3072-bit safe prime).
>     * Needs a fast modular multiplication/inverse implementation.
>     * Using SHA512 + ChaCha20 for generating the hashes takes 1.2us per element.
>     * Modular multiplication using GMP takes 1.5us per element (2.5us
> with a 60-line C+asm implementation).
>     * 768 bytes for maintaining a running sum (384 for numerator, 384
> for denominator)
>     * Very common security assumption. Even if the DL assumption would
> be broken (but no k-sum algorithm faster than Wagner's is found), this
> still maintains 110 bits of security.
> 2. (ECMH) Adding secp256k1 EC points
>     * Much more complicated than the previous approaches when
> implementing from scratch, but almost no extra complexity when ECDSA
> secp256k1 signature validation is already implemented.
>     * Using SHA512 + libsecp256k1's point decompression for generating
> the points takes 11us per element on average.
>     * Addition/subtracting of N points takes 5.25us + 0.25us*N.
>     * 64 bytes for a running sum.
>     * Identical security assumption as Bitcoin's signatures.
> 
> Using the numbers above, we find that:
> * Computing the hash from just the UTXO set takes (1) 2m15s (2) 9m20s
> * Processing all creations and spends in an average block takes (1)
> 24ms (2) 100ms
> * Processing precomputed per-transaction aggregates in an average
> block takes (1) 3ms (2) 0.5ms
> 
> Note that while (2) has higher CPU usage than (1) in general, it has
> lower latency when using precomputed per-transaction aggregates. Using
> such aggregates is also more feasible as they're only 64 bytes rather
> than 768. Because of simplicity, (1) has my preference.
> 
> Overall, these numbers are sufficiently low (note that they can be
> parallellized) that it would be reasonable for full nodes and/or other
> software to always maintain one of them, and effectively have a
> rolling cryptographical checksum of the UTXO set at all times.
> 
> ### 4. Use cases
> 
> * Replacement for Bitcoin Core's gettxoutsetinfo RPC's hash
>   computation. This currently requires minutes of I/O and CPU, as it
>   serializes and hashes the entire UTXO set. A rolling set hash would
>   make this instant, making the whole RPC much more usable for sanity
>   checking.
> * **Assisting in implementation of fast sync methods with known good
>   blocks/UTXO sets.**
> * Database consistency checking: by remembering the UTXO set hash of
> the past few blocks (computed on the fly), a consistency check can be
> done that recomputes it based on the database.

* Full discussion:
  * Initial: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2017-May/014337.html
  * Last: https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2017-May/014402.html

### Pros

- using the same group as bitcoin is already using we have a solid implementation
  already (secp256k1)
- having the rolling hash available can improve other areas of bitcoin
  (as outlined on the mailinglist, `gettxoutsetinfo` can benefit from it as well
  as consistency checks of the leveldb database)
- does not introduce any complicated consensus rules such as altering the
  finalization protocol for supporting snapshots
  
### Cons

- has to be included in every block
  - combat: could be alleviated by only including it in every k-th block (checkpoints
    for example) and looking back those last _k_ blocks.
- increases the size of the blockchain
  - combat: not much, also could be included only every k-th block
- makes it mandatory for proposers to calculate the incremental checksum
  - combat: this computation is cheap and has the potential to simplify other
    computations

## Decision

The incremental utxo set's hash is included in every block's coinbase transaction
and can be used for verifying downloaded snapshots. The hash can be updated incrementally
by adding the created and deleting the spent transactions, using ECMH. This computation
is cheap enough (and has further benefits) that it can be done by all nodes. Also it
can be done by looking at the previous block without having the full UTXO set.

## Consequences

Each block (or every k-th block) grows by 32 bytes (256 bits).

# Previous Discussion

## Slack

```
Julian [12:25 PM]
The motivation for this approach is that the snapshot feature is supposed to be
optional, so you can’t query every server for it and there’s also no incentive
for anyone to have snapshots available (except that for the network as a whole
it might be better to exchange more snapshots instead of full copies of the
blockchain -> less bandwidth used). This is why I was looking for a way for
everyone to have a snapshot hash for any block height available, but it should
be cheap to do so. Embedding it in the coinbase transaction makes it part of the
validation/consensus rules, but the check should be cheap as you can look at the
previous block and the UTXOs created/spent and calculate the next hash from it.
Optionally that can be relaxed to only be included in every Nth block but it
also requires to look back these N blocks.

amiller [4:36 PM]
Yeah, i think that makes sense. It's definitely preferable if it's available to every node based on consensus rules and not merely optional, as long as it's not burdnesome to include in consensus rules
So why muhash instead of ecmhash?

Julian [4:40 PM]
To quote from that mailing-list
> Note that while (ECMH) has higher CPU usage than (MuHash) in general, it has
> lower latency when using precomputed per-transaction aggregates. Using such
> aggregates is also more feasible as they’re only 64 bytes rather than 768.
> Because of simplicity, (1) has my preference. _–Pieter Wuille_
Also we found -> https://eprint.iacr.org/2009/168.pdf in ->
https://en.bitcoinwiki.org/wiki/Elliptic_curve_only_hash#Second_pre-image_attack

amiller [4:43 PM]
That attack is not applicable to ECMH right?

Julian [4:45 PM]
Right. We might have mixed that up in the discussion :-X

amiller [4:45 PM]
Algebraically muhash and ecmh are exactly the same, just in one case the group
is a schnorr group (prime order subgroup of Fp for p a 3072 prime) and in the
other the group is secp256k1

Julian [4:46 PM]
In terms of simplicity of the implementation that’s probably even preferable
and we can explain it better as that’s the same group which is already used
in bitcoin

amiller [4:46 PM]
IMO that's the way to go

amiller [4:46 PM]
It's also easier I think to hash to an exponent in secp256k1 (edited)
The nice property of secp256k1 is that the order is very close to 256 bits
```

## XOR Proposal (rejected, unsafe)

*This section is informational and preserved only to reflect the discussion which has
gone into this issue.*

**Update:** *combining hashes using XOR is unsafe as a the <i>Subset XOR</i> problem is
easily solvable by gaussian elimination. That way a subset of hashes that XOR to a given
value (zero) could be just eliminated from the snapshot.*

This proposal is to incrementally compute a checksum of the current UTXO set and
publish it with every block. Since that would be part of the protocol and every node
would have to do it this computation should be cheap and must not rely on having a full
copy of the blockchain or an existing snapshot available (otherwise we might face a
chicken and egg problem).

A UTXO set is a set of UTXOs. Each UTXO is identified by the transaction it is contained
in and the index in that transaction. Hence a possible _utxo id_ is (_txout id_ really):

> utxo-id := SHA256(transaction-id || txout-index)

The checksum of a full UTXO set of size _N_ can be defined as (⊕ is XOR):

> utxo-set-checksum := utxo-id-1 ⊕ ... ⊕ utxo-id-N

Using XOR allows to incrementally build the `utxo-set-checksum` from a previous block.
Each block contains the `utxo-set-checksum` of the utxo-set at its block height in the
coinbase transaction (much like its own block height and the Proof of Stake signing key
are included in the coinbase transaction).

```
    BLOCK       TRANSACTIONS      SPENT    CREATED      UTXO SET
    -----       ------------      -----    -------      --------
in:
    Block-0
out:            u0 u1 u2 u3 u4             {u0, u1, u2, u3, u4}

                                                        {u0, u1, u2, u3, u4}
                                                        
in:             u0 u2    u4       {u0, u2, u4}
    Block-1      \ /   / | \
out:             u5  u6 u7 u8              {u5, u6, u7, u8}

                                                        {u1, u3, u5, u6, u7, u8}
```

The checksum of the UTXO set at height=0 is

> utxo-id(u0) ⊕ utxo-id(u1) ⊕ utxo-id(u2) ⊕ utxo-id(u3) ⊕ utxo-id(u4)

The checksum of the UTXO set at height=1 is

> utxo-id(u1) ⊕ utxo-id(u3) ⊕ utxo-id(u5) ⊕ utxo-id(u6) ⊕ utxo-id(u7) ⊕ utxo-id(u8)

The checksums of the UTXO sets of spent and received txouts are:

> spent: utxo-set-checksum({u0, u2, u4}) = utxo-id(u0) ⊕ utxo-id(u2) ⊕ utxo-id(u4) <br>
> created: utxo-set-checksum({u5, u6, u7, u8}) = utxo-id(u5) ⊕ utxo-id(u6) ⊕ utxo-id(u7) ⊕ utxo-id(u8)

The UTXO set checksum at height=N+1 can be computed from the utxo set checksum at
height=N by:

> utxo-set-checksum(N) ⊕ utxo-set-checksum(spent at N+1) ⊕ utxo-set-checksum(created at N+1)


