# BIP removal reference

This document contains code references to all the BIP that are considered active from the initial release.

## [BIP30](https://github.com/bitcoin/bips/blob/master/bip-0030.mediawiki)

 [[a8afc6c](https://github.com/dtr-org/unit-e/commit/a8afc6c)] - This commit removes checks for duplicated txids from different transactions, this is now impossible (since [BIP34](https://github.com/bitcoin/bips/blob/master/bip-0030.mediawiki) is in force).

## [BIP22](https://github.com/bitcoin/bips/blob/master/bip-0022.mediawiki) and [BIP23](https://github.com/bitcoin/bips/blob/master/bip-0023.mediawiki)

[1dfe8695](https://github.com/dtr-org/unit-e/commit/1dfe86954be1ea0d1d42dcf9d2f9606a0ac40ab9) – This commit
removes BIP22 and BIP23 as in a Proof-of-Stake setting we do not have mining pools and therefore no use for supporting blocktemplates.

