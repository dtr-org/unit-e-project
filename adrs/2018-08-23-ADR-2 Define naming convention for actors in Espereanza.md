# ADR-2: Define naming convention for actors in Esperanza
```
Status: Accepted
Created: 2018-08-23
Accepted: 2018-08-24
```
## Context
We have to maintain a consistent naming in the codebase for roles in the Esperanza protocol.  
At the moment we have plenty of examples where there is confusion especially when mixing terms like `staking`, `miner`, `proposer`.  

## Decision
We outline two clear actors in the protocol:
- The `PROPOSER`: which solves the function of proposing new blocks through his stake. At the moment words like `staking`, `miner`, `mining` are associated with the same function.

- The `VALIDATOR`: which takes active part in the finalisation process with the voting.

We therefore MUST replace:
- all the instances of `miner` with `proposer`.
- all the instances of `mining` with `proposing`.
- all the instances of `staking` with `proposing`.

But we MUST NOT replace the instances of the word `stake` since this indicates the actual deposit made in order to propose.  
The only exception to this is `stakethread.h` that MUST be renamed to `proposerthread.h`.

## Consequences
A more coherent and consistent naming convention will help readability and avoid confusion.
