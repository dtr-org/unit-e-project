# ADR-3: Unit-e Block Header to include SegWit Merkle Root

```
Status:   Accepted
Created:  2018-08-23
Accepted: 2018-09-04
```

## Context

Unit-e is a fork of [bitcoin-core](https://github.com/bitcoin/bitcoin) and uses the "esperanza"
Proof-of-Stake consensus protocol instead of Bitcoin's Proof-of-Work scheme. The design is inspired
by "PoS v3" with Ethereum's "Casper FFG". The implementation is based on
[particl-core](https://github.com/particl/particl-core).

The differences between these protocols and lessons learned during the development of bitcoin
make us consider changes from the original bitcoin header format.

### Bitcoin block header

The bitcoin block header is 80 bytes:

```
   0  vvvv pppp pppp pppp
  16  pppp pppp pppp pppp
  32  pppp mmmm mmmm mmmm
  48  mmmm mmmm mmmm mmmm
  64  mmmm tttt bbbb nnnn
```

<dl>
  <dt>vvvv : 4 bytes (int32_t)</dt>
  <dd>block version number</dd>
  <dt>pppp... : 32 bytes (uint256)</dt>
  <dd>previous block hash</dd>
  <dt>mmmm... : 32 bytes (uint256)</dt>
  <dd>merkle tree root</dd>
  <dt>tttt : 4 bytes (uint32_t)</dt>
  <dd>timestamp</dd>
  <dt>bbbb : 4 bytes (uint32_t)</dt>
  <dd>bits (difficulty)</dd>
  <dt>nnnn : 4 bytes (uint32_t)</dt>
  <dd>nonce</dd>
</dl>

### Particl block header

The bitcoin block header is 112 bytes:

```
   0  vvvv pppp pppp pppp
  16  pppp pppp pppp pppp
  32  pppp mmmm mmmm mmmm
  48  mmmm mmmm mmmm mmmm
  64  mmmm wwww wwww wwww
  80  wwww wwww wwww wwww
  96  wwww tttt bbbb nnnn
```

The additional field is:

<dl>
  <dt>wwww... : 32 bytes (uint256)</dt>
  <dd>segregated witnesses merkle root</dd>
</dl>

### SegWit in Bitcoin

[Peter Wuille](http://pieterwuillefacts.com/) explains some design decisions regarding SegWit in
Bitcoin on [Bitcoin StackExchange](https://bitcoin.stackexchange.com/a/58415/83940):

> **Why the witness Merkle root is stored in the coinbase: easiest deployment for miners**
> 
> Lastly, we need a place to embed the witness Merkle root hash that affects the block hash. **_Using the block header would have been perfect_**, but there is no way to add data there without breaking every piece of Bitcoin infrastructure.
> 
> The only place flexible enough for storing that data is in a transaction. A special transaction could have been added which contains the commitment, but transactions bring extra overhead. They need inputs and outputs, which need to come from somewhere and go somewhere.
> 
> Because of that, the only choice remaining was to embed the commitment in an existing transaction. The coinbase transaction is the logical choice - it is already created by miners anyway, and adding a dummy output to it has low resource costs (due automatic removal of OP_RETURN outputs from the UTXO set).

## Decision

We will adopt the particl block header structure, which makes the witness merkle root part of the block header.

## Consequences

As Peter Wuille points out:

> there is no way to add data there without breaking every piece of Bitcoin infrastructure

Doing this change in bitcoin would require the coin to hardfork. Luckily we're not live yet,
so we can still do such a breaking change in unit-e. It will require us to change most of the
tests though (especially the fixtures), which requires a bit of effort from our side.




