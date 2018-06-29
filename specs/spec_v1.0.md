# **Summary**
The goal of this document is to explain with a reasonable level of detail the specification for Unit-e v1.0 .

# **Block proposal**
The block proposal is the process to create the next block of the blockchain and it is constituted of three parts: **management of valid proposers**, **selection of block proposer**, and **block proposal** itself.

## Proposer permissioning
As a safeguard, we will initially use permissioning to whitelist eligible proposers. This will gradually be relaxed. For initial development, we will have a hardcoded list in the codebase of public keys for eligible proposers. The PKI will be managed by administrative transactions.

## Proposer selection
We will use a distributed mechanism for choosing proposer, where every proposer node (that owns one of the public key registered in the proposer whitelist) will hash key, next block height, and previous block hash. The node is elected for the current round if the hash result is below a certain threshold (defined so that every whitelisted proposer has the same chance to be elected).

Following some pseudo-code that illustrates the election algorithm.
```python
blockHeight = curBlockHeight   # round counter
difficulty = 1/numValidators  # probability of a node being elected leader (chosen to avoid collisions as much as possible)

while (true) {
	nNow = GetTime() 	        		# current time
	nextRoundTime = nNow + BLOCK_TIME		# time of next round
	myRandNum = Hash(myKey, block_height, prev_block_hash)
	normRandNum = myRandNum / MAX_HASH  # define MAX_HASH so that 0 <= normRandNum <= 1
	if (normRandNum < difficulty) {
		# propose a block (details in next subsection)
		...
	}

	# wait until the next round starts
	nNow = GetTime()
	wait(nextRoundTime - nNow)
	blockHeight += 1
}
```
MAX_HASH should change over time to account for a change in number of active proposer.

## Block proposal
The elected proposer now has the duty to:

* build a new block including transactions from his mempool
* create a new coinbase transaction (still to define how this is used)
* broadcast the new block to the peers

Is not yet defined exactly how rewards to validators and proposers are composed or what is their magnitude, if relative to the total stake at a given time or relative to the staked amount. Such details need to be defined, if not immediately, at least before release.

To prove that a proposer has been rightfully elected any node can simply recompute the hash explained above and check it against the difficulty parameter of the previous block.

```python
# activeChains = data structure with existing, unfinalized chains

chosenChain = null
# proposer builds on the longest justified chain
for (chain in activeChains):
	if (isJustified(chain.lastCheckpoint)) and (length(chain) > length(chosenChain)):
		chosenChain = chain
}
myBlock = BuildBlock(chosenChain, transactions)
chosenChain.append(myBlock)
broadcast(myBlock)
```

# **Block finalization**
Blocks are not finalized in Particl or Bitcoin, so this portion of the algorithm will require the most changes. To support this we need few basic functionalities or primitives: (1) deposit, (2) voting, (3) slashing, (4) logout, (5) withdraw. Our design choices are modeled heavily on Casper implementation.

At the moment we don't foresee any changes to the block header or internal structure.

This implementation relies heavily on statefulness of the consensus. This means that all the nodes in order to be able to accept blocks and transactions need to have an up-to-date view of the whole consensus state. The state structure is drafted with big contributions from the Casper contract code base with some simplifications.

```bash
class Validator {
  deposit: decimal, # current validator deposit
  start_dynasty: int, # index of the dynasty since the validator is included
  end_dynasty: int, # index of the dynasty till the validator is included
  is_slashed: boolean, # if the validator has been slashed
  total_deposits_at_logout: int, # the value of the
  addr: address # validator address
}
```

```bash
class Checkpoint{
    cur_deposits: int, # total deposit for this checkpoint
    cur_votes: int, # total deposit that has voted for this checkpoint
    votes_map: map, # map of which validator IDs have already voted
    is_justified: bool, # is the checkpoint justified
    is_finalized: bool # is the checkpoint finalized
}
```
a possible casper state implementation inside Particl

```bash
validators[] # list of the current validators
checkpoint_hashes # map <epoch_index, checkpoint_hash>
validator_addr # map <validator_index, validator_addr>
total_cur_dyn_deposit # total deposit for the current dynasty
dynasty # the index of the current dynasty
dystay_in_epoch # map <dyn_index, epoch_index>
```

## 1. Deposit transactions

Casper validators deposit funds into a smart contract. Since we do not directly support smart contracts, we will instead implement a new "deposit" transaction type that locks the funds for a certain amount of `dynasties` and proves that the node is participating in the voting process. There is no other way to spend this transaction than using a logout transaction or a vote transaction.

### 1.1 Deposit transaction data

* `version` - is used to distinguish this transaction as a separate type. Its value is 3 for this transaction type.
* `Input(s)` - as any normal transaction, no special rules or limitations here.
* `Output` - the transaction has one single output and the `ScriptPubKey` must contain a specific script. The minimum value must be `MIN_DEPOSIT_SIZE`. Fees are allowed as usual. It makes sense to pay the transaction to an address under the depositor control.
  * `ScriptPubKey` this field has to contain a special script that allows slashing (see 1.2). The content of the script must be validated at least by the `proposers`.
* `Locktime` - is not used.


#### 1.2 Deposit script
In order to provide vote and slash functionalities on top of a deposit transaction we need to extend the current script language with new op_codes.

Let's define `VTXn` is the tuple `<s, t, h(s), h(t)>` so that
```
s     is the TXID of any justified checkpoint ("source")
t     is the TXID of any descendant of 's' ("target")
h(s)  the block height of s
h(t)  the block height of t
```
and `SIGn` is the signature from the validator private key of `VTXn`.

`OP_CHECKVOTESIG`:
- consumes the first 3 elements of the stack as <SIG, VTX, PUBKEY>
- pushes back the result of PUBKEY_DECRYPT(SIG) == HASH256(VTX)

`OP_SLASHABLE`:
- consumes the first 5 elements of the stack as <SIG1, VTX1, SIG2, VTX2, PUBKEY>
- executes OP_CHECKSIG(SIG1,VTX1,PUBKEY)
- executes OP_CHECKSIG(SIG2,VTX2,PUBKEY)
- executes SIG1 == SIG2
- checks
```python
height(VTX1) == height(VTX2) or   
(target(VTX1) > target(VTX2) and source(VTX1) < source(VTX2)  or target(VTX2) > target(VTX1) and source(VTX2) > source(VTX1))
```
- pushes back `TRUE` if all the previous checks succeeded, `FALSE` otherwise.

```
# Vote verification script
OP_OVER
OP_OVER
OP_PUSHDATA1 PUBKEY
OP_CHECKVOTESIG

OP_IF
OP_TRUE

OP_ELSE
# Common P2PKH
OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG

OP_ELSE
# The script that allows this tx to be spent by a violation reporter
OP_PUSHDATA1 PUBKEY
OP_SLASHABLE
OP_ENDIF
```
using this script in the deposit for someone to slash the deposit is sufficient to provide a `scriptSig` like
```
<VTX1> <SIG1> <VTX2> <SIG2>
```
for vote and logout operations is simply
```
<VTX> <SIG>
```
for withdrawing instead a normal P2PKH is sufficient
```
<sig> <pubKey>
```

## 1.3 Validating a deposit transaction
When receiving a deposit transaction a node should in addition to the regular transaction checks do the following:

* check if the address from where the deposit is sent is already a validator.
* check that the deposit output value is >= MIN_DEPOSIT_SIZE.
* save a new validator object to store the state information of this new validator.

```
{
  "deposit" : output_value,
  "start_dynasty": cur_dynasty + 2,
  "end_dynasty": infinity,
  "is_slashed": false,
  "total_deposit_at_logout": 0,
  "address": addr
}
```
* save the validator withdrawal address for future reference.
* update the current dynasty total deposit.

The `"start_dynasty": cur_dynasty + 2` should give enough time to the deposit to be included in a block and broadcasted to all the nodes.

## 2. Vote transactions

Votes will be casted with a new type of transaction. All votes should be added to the blockchain, regardless of which fork they support.  
We have not yet considered how to incentivize proposers to include votes in their blocks; most likely, we will have to set apart separate space in each block for votes (as opposed to regular transactions).  
For now, we are assuming that the (permissioned) proposers will behave properly and include votes in blocks.

A validator is  supposed to vote once per epoch; if this does not happen then it will be charged of s penalty for being offline.  
The accumulated `offline penalty` over time will be applied when a node tries to rightfully spend its deposit after logout.  
At withdrawal a validator will be able only to retrieve the portion of the deposit remaining after the total `offline penalties` are applied.

Votes can either spend a deposit transaction, another vote transaction, a logout transaction or a withdraw; for the vote transaction to be valid it is necessary for the only output to have the same `ScriptPubKey` of the spent transaction and a value equal to the spent transaction plus the reward for the vote performed.  
In this way we will create a chain of transactions with at the beginning a deposit transaction and at the end a withdraw or a slash transaction.  
Such chain will allow to compound deposit and rewards at each round till a slash or a withdraw happens.

### 2.1 Vote transactions data
Vote transactions are a special type of transaction.

* `version` - is used to distinguish this transaction as a separate type. Its value is 4 for this transaction type.
* `Input(s)` - the transaction is going to have only one input.
  * `TXID` - is the reference to the previous deposit, vote or logout transaction.
  * `VOUT` - this should be 0, since logout, deposit and vote transactions have only one output.
  * `ScriptSig` - this field contains the data `<s, t, h(s), h(t), sig>` serialized in this order as consecutive bytes.
* `Output` - the transaction has a single output and the `ScriptPubKey` must contain a specific script. The value has to be the same as the deposit plus the calculated reward. Fees are not allowed.
	  * `ScriptPubKey` this field has to contain a special script that allows slashing (see 1.2). The content of the script must be validated at least by the `proposers`.
* `Locktime` - is not used.

Furthermore a vote transaction can be spent only by a logout transaction, another vote transaction, a slash transaction or a withdraw transaction.

### 2.2 Validating a vote transaction

In order to validate a vote transaction a node should:

* check if the validator already voted for this target epoch.
* check that the target epoch and the target hash are the ones expected.
* check that the source epoch is justified.
* check that the validator is part of validator set of the current or previous dynasty (if not logged out and has an active deposit).
* record the vote.
* increment the `total_cur_dyn_deposit`.
* if enough votes are registered justify the checkpoint and finalize the previous one.

For each valid vote a validator should receive a reward, this is compounded along with the deposit and is part of the stake of the validator. At withdrawal the validator will be able to claim the deposit and all the vote rewards.

## 3. Slashing transaction

In Casper, it is up to the block proposers to include slashing transactions that punish bad actors, and the first node that reports the bad behaviour gets the bounty. We will again implement a special transaction that provides evidence of the slashing conditions being violated (see deposit transactions).

## 3.1 Slashing transaction data

This transaction simply needs to provide the correct inputs to the validator’s deposit transaction, and the outputs are as normal. We are calling this a separate transaction type mainly for readability and ease of parsing in the blockchain; its functionality is not different from standard transactions.

* `version` - is used to distinguish this transaction as a separate type. Its value is 5 for this transaction type.
* `Input(s)` - the transaction is going to have only one input and this will be a deposit, vote or logout transaction.
  * `TXID` - is the reference to a deposit, vote or logout transaction which output is unspent.
  * `VOUT` - this should be 0.
  * `ScriptSig` - this should include the proof of the offending votes (see 1.2).
* `Output` - as a normal transaction the outputs can be multiple but the first output must "burn" using an `OP_RETURN` in the pubkey at least `SLASHING_BURN_FRACTION` of the deposit.
* `Locktime` - is not used.

### 3.2 Validating a slashing transaction

* execute the script as usual to verify that the deposit is unlocked.
* mark the validator as slashed and log it out forcefully.

## 4. Logout transaction
In order to get back the deposit a validator has to send a logout transaction.  
The block in which this transaction is included is used to set the `end_dynasty` for the validator using `cur_dinasty + LOGOUT_DELAY`.

## 4.1 Logout transaction data
This transaction is basically the same as a deposit transaction with the exception that only a deposit or a vote transaction can be the input.

* `version` - is used to distinguish this transaction as a separate type. Its value is 6 for this transaction type.
* `Input(s)` - the deposit or vote transaction.
* `Output` - the transaction has one single output and the `ScriptPubKey` must contain a specific script. The value has to be the same as the deposit or vote used. Fees are allowed as usual. It makes sense to pay the transaction to an address under the depositor control.
  * `ScriptPubKey` this field has to contain a special script that allows slashing (see 1.2). The content of the script must be validated at least by the `proposers`.
* `Locktime` - is not used.

## 5. Withdrawing transaction
This transaction is a special transaction that spends the logout transaction. The only difference is that in order to be valid it has to happen after `WITHDRAWAL_DELAY` and its value has to be equal to the `deposit - non_voter_penalties + vote_rewards`.

## 5.1 Withdrawing transaction data
This transaction is basically a normal transaction except the fact that has to have a logout transaction as input and that the total amount payed in the output can be different from the original deposit because of penalties and rewards.

* `version` - is used to distinguish this transaction as a separate type. Its value is 7 for this transaction type.
* `Input(s)` - the logout transaction.
* `Output` - as a normal transaction the outputs can be multiple.
* `Locktime` - is not used.


# Parameters values

* `BLOCK_TIME`: 4 seconds

* `MIN_DEPOSIT_SIZE`: TBD

* `NON_REVERT_MIN_DEPOSIT`: TBD

* `LOGOUT_DELAY`: TBD

* `WITHDRAWAL_DELAY`: TBD

* `SLASHING_BURN_FRACTION`: 0.96


# **Glossary**

* **epoch:** The span of blocks between checkpoints. Epochs are numbered starting at the hybrid casper fork, incrementing by one at the start of each epoch.

* **finality:** The point at which a block has been decided upon by a client to never revert. Proof of Work does not have the concept of finality, only of further deep block confirmations.

* **checkpoint:** The block/hash under consideration for finality for a given epoch. This block is the last block of the previous epoch. When a checkpoint is explicitly finalized, all ancestor blocks of the checkpoint are implicitly finalized.

* **validator:** A participant in the consensus protocol that has deposited *ees* on the blockchain and has the responsibility to vote and finalize checkpoints.

* **validator set:** The set of validators for a given dynasty.

* **block proposer:** A node whose role is to participate in the proposer's election. When elected for the current round it proceeds to create a new block and broadcast it to the other nodes. This function is very similar to the one miners are fulfilling in a PoW protocol.

* **block proposer set:** The set of proposers allowed to be elected for a proposing round.

* **proposing round:** A time slot in which one block proposer is elected to propose the next block.

* **block proposer whitelist:** A predefined list public key of allowed block proposers.

* **dynasty:** The number of finalized checkpoints in the chain from root to the parent of a block. The dynasty is used to define when a validator starts and ends validating. The current dynasty only increments when a checkpoint is finalized as opposed to epoch numbers that increment regardless of finality.

* **slash:** The burning of some amount of a validator's deposit along with an immediate logout from the validator set. Slashing occurs when a validator signs two conflicting vote messages that violate a slashing condition.

* **offline penalty:** In the case that a validator doesn't vote during an epoch then it should be punished removing a penalty from its deposit.