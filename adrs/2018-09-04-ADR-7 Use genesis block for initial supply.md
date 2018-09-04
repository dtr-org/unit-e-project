# ADR-7: Use genesis block for initial supply
```
Status: Accepted
Created: 2018-08-30
Accepted: 2018-09-04
```
## Context
We need a way to provide initial supply. At the moment it is not possible to spend the genesis block coinbase because
even if the block is added to the index, its transactions are not added to the txdb.

## Decision
We want to change the code so that we are able to create an initial supply but we MUST only use the coinbase of the
genesis block and MUST NOT resort to further `imports` in subsequents blocks like for example Particl did.

All the coins of the initial supply MUST be minted in the coinbase transaction of the genesis block.

## Consequences
We will have an easy and transparent way of creating initial supply.
