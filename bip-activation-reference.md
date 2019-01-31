# BIP removal reference

This document contains code references to all the BIP that are considered active from the initial release.

## [BIP30](https://github.com/bitcoin/bips/blob/master/bip-0030.mediawiki)

 [[a8afc6c](https://github.com/dtr-org/unit-e/commit/a8afc6c)] - This commit removes checks for duplicated txids from different transactions, this is now impossible (since [BIP34](https://github.com/bitcoin/bips/blob/master/bip-0030.mediawiki) is in force).

## [BIP22](https://github.com/bitcoin/bips/blob/master/bip-0022.mediawiki) and [BIP23](https://github.com/bitcoin/bips/blob/master/bip-0023.mediawiki)

[1dfe8695](https://github.com/dtr-org/unit-e/commit/1dfe86954be1ea0d1d42dcf9d2f9606a0ac40ab9) – This commit
removes BIP22 and BIP23 as in a Proof-of-Stake setting we do not have mining pools and therefore no use for supporting blocktemplates.

# BIPs enabled by default

## [BIP16](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki) – P2SH

BIP16 (P2SH) is enabled by default. Enabling it by default simply got rid of redundant checks, as P2SH is not even an option in unit-e (because of the native/default usage of segwit we do P2WSH, and that's already there inconditionally (i.e. without any special BIP16 checks)).

BIP16 was activated by default in [#523](https://github.com/dtr-org/unit-e/pull/523).

## [BIP34](https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki) – Height in Coinbase

BIP34 was made a consensus rule via a soft fork. Since we are starting from scratch, BIP34 is enabled by default.

Since the block building and validation logic are rewritten for Proof-of-Stake this BIP is handled completely differently than in bitcoin; also our coinbase transaction looks different.

The bitcoin-style BIP34 was removed in [#522](https://github.com/dtr-org/unit-e/pull/522).

## [BIP65](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki) – CLTV

BIP65 (`CHECKLOCKTIMEVERIFY`) was rolled out as a softfork just like BIP34 and is enabled by default in unit-e.
This affects the scripting system which is largely untouched in unit-e.

BIP65 was enabled by default in [#521](https://github.com/dtr-org/unit-e/pull/521).

## [BIP66](https://github.com/bitcoin/bips/blob/master/bip-0066.mediawiki) – DERSIG

BIP66 (Strict DER Signatures) was rolled out as a softfork just like BIP34 and BIP65. It is very similar to BIP65
with regards to the way it was rolled out and how functional tests are written.

BIP66 was enabled by default in [#503](https://github.com/dtr-org/unit-e/pull/503).

That pull request also removed the `softforks` information from the `blockchain` RPC call. Softfork information continues to be reported (bip9 softforks).

