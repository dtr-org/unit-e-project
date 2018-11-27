# ADR-12 Fork choice rule

```
Status:   Accepted
Created:  2018-10-17
Accepted: 2018-10-25
```

## Context

Bitcoin follows simple fork-choice rule: every time, it switches the active chain to the hardest one. Unit-E
adapts [Casper](https://arxiv.org/pdf/1710.09437.pdf) ideas. Validation (Finalization and Justification parts)
is already implemented, now we need to implement Casper's fork-choice rule.

## Decision

Casper stands the following fork-choice rule:

> Follow the chain containing the justified checkpoint of the greatest height.

Since we built on top of Bitcoin we need to adapt its fork-choice rule to take justification and finalization
into account. The high-level algorithm is:

```
# Few hints:
# block        is a new block
# chain        is the chain `block` belongs to
# active_chain is an active chain
# IsTip()      returns if block is a tip of any chain
# Discard()    discard the `block`, don't connect to any chain
# Switch()     switch to the `chain` (or connect the `block` to active chain in case the block is
               built on the top of it)
# Store()      Store the `block` in the `chain`.

if LastFinalizedEpoch(chain) < LastFinalizedEpoch(active_chain)
  Discard(block)
else
  if IsTip(block)
    if LastJustifiedEpoch(chain) > LastJustifiedEpoch(active_chain)
      Switch(chain)
    else # -- bitcoin rule --
      if GetChainWork(chain) > GetChainWork(active_chain)
        Switch(chain)
      else
        Store(block)
  else
    Store(block)
```

In the algorithm above `-- bitcon rule --` marks the if-else branch that follows usual bitcoin fork-choice
rule. It's mean that we can build our rule on the top of bitcoin one by implementing several additional checks
prior.

### More details

For now we have FinalizationState (holds finalization and justification details) for the active chain only.
In order to be able to compare justified/finalized epochs from different chains we need to have per-chain
states. After we reach the next finalization point we need to:

* Delete FinalizationState-s of concurrent chains;
* Delete all blocks that don't belong to the active chain.

## Consequences

We will follow Casper fork-choice rule as a main rule and consider bitcoin rule on the last step only.

This change will lead to failure of some of bitcoin tests we will have to adapt to the new rule. It's
important to not just disable or rewrite old tests because they check behavior we're still following, instead
we have to leave old tests as is with little working arounds (for example we can run tests with large EpochLength
or we can disable Finalization mechanism by activating and stopping validator).
