# Slashing in finalization

Slashing is the process of punishing a misbehaving validator after having
detected a slashable condition.

In order to slash a validator a node needs to create a transaction that contains
unequivocal proof that a specific validator broke one of the slashing conditions
and have this transaction included in a block.

This mechanism is extremely important for the security of the network. In [1] is
demonstrated how it is impossible to finalize two concurrent chains without having at
least one 1/3 of the validator slashed. If the slashing mechanism does not work
properly we lose the _accountable safety_ property.


### Slashing conditions
There are two slashing conditions:

- a validator cannot vote for two different checkpoint hashes at the same height. This is called
`double-vote`.
- defined `source(v)` as the height of the source epoch in  vote `v`, and
defined `target(v)` as the height of the target epoch in  vote `v` then
a validator cannot send `surrounding votes` such as  
`source(v1) > source(v2) && target(v1) < target(v2)` or  
  `source(v1) < source(v2) && target(v1) > target(v2)`.


### Slash transaction
A node can provide proof of a validators' slashable behavior creating a special
transaction called `Slash Transaction`.

This transaction has a very specific format:
- It must spend the last finalization transaction of the validator to be slashed.
- It needs to provide an unlocking script (`scriptSig`) that contains both the votes
that proof misbehavior.  
 The script looks like `< txSig <vote1Sig, vote1> <vote2Sig, vote2> >`,
wher `txSig` is the transaction signature, `voteXSig` is the signature of the vote `X`
made with the validator's private key and `voteX` is the serialized form of the vote `X`.
- It must burn the whole validator's current deposit (which is the amount of the
last finalization transaction created by it).
- The transaction has no fees.

This transaction by construction is not "owned" by anybody, and the first node
that, after having seen it can propose a block, will be able to include it as
its own, utilizing the proof given to effectively slash the validator. This
though is not the client default behavior and doing so does not provide any
benefit, so the rational node will just include it as is.

No reward for including the slashing transaction is defined at the moment.

The creation of the slash transaction is handled in `WalletExtension::SendSlash()`
that accepts as parameters the two votes that are proving the misbehaviour.
Then the function proceeds as follows:

- creates a new transaction with `TxType:SLASH`.
- two votes that represent the slash proof are encoded in the `scriptSig`.
- the last known finalization transaction made by the validator is fetched and used
as input.
- a new output burning all the `prevTx` amount is added.
- signs the transaction.
- calls `CommitTransaction()` on the wallet.

In order to avoid fee filtering we had to circumvent checks made in `net_processing.cpp`
against the `filterrate` that prevents relaying transactions with less than some `minFee`.
In `validation.cpp` within `AcceptToMemoryPoolWorker()` we also have to make sure
to set `bypass_limits` to allow fee limits checks to be skipped.


### Slash validation

Like all finalization transactions, slash transactions are validated in two places:

In `validation.cpp`
- inside `AcceptToMemoryPoolWorker()` almost at the end of the whole
function since the transaction has first to adhere to many general transaction
format rules.
- inside `ContextualCheckBlock()` while iterating over all the transactions of the
block to make sure that they are final (if they have a locktime that is in the past).

The function used for both checks in `esperanza/validation.cpp` and is called
`esperanza::CheckSlashTransaction()` there it:
- checks the number of `vin` and `vout` to be 1.
- calls `isSlashable()` with them.

If one of the checks is not successful the function returns `false` and increases
the DoS value for the peer by 10.

Signatures and the script is actually checked (as usual) inside `AcceptToMemoryPoolWorker()`
or inside `CheckTxInputs()` called by `ConnectBlock()`.


### Slashing conditions detection

A very important part of the slashing mechanism is the efficient recognition of
misbehaviours. In order to do so all nodes will have to keep track of all the
votes cast by the currently active validator set.

Since we need to record votes that are potentially not even part of the current
blockchain we have to eagerly evaluate votes in `CheckTransaction` in `validation.cpp`
and register them in the `VoteRecorded`.


##### Vote Recoder

This class has the duty of registering votes and spot slashable behaviors. This
class is a singleton object, which instance can be retrieved by calling `VoteRecorder::GetVoteRecorder()`.

The singleton instance is initialized during the application boostrap in `init.cpp`
where `VoteRecorder::InitVoteRecorder()` is being called.

Whenever a vote transaction is detected `VoteRecorded::RecordVote()` should be
called, this internally registers the vote and searches for a possible double or
surrounding vote. If one is found, it means we can proceed with slashing the validator.

Both the votes are then passed to `GetMainSignals().SlashingConditionDetected()`.
The listening interface is implemented by the wallet in `SlashingConditionDetected()`,
that does few checks and then calls `SendSlash()` to create and commit the slash
transaction.


### Finalization State effects

Two functions are responsible for validating and processing a slash transaction.

`FinalizationState::IsSlashable` checks that:
- the votes passed are belonging to validators.
- they don't belong to the same validator.
- they are not the same vote.
- the validator is already part of the validator set.
- the validator wasn't already slashed.
- the votes are actually a double vote or a surrounding vote.

`FinalizationState::ProcessSlash` :
- marks the validator as slashed.
- removes the validator from the validator set.
- removes the validator's deposit from the `current_dynasty_delta`.

## References

[1] V. Buterin and V. Griffith, “Casper the friendly finality gadget,” URL
https://arxiv.org/pdf/1710.09437.pdf, 2017.
