# ADR-9 Validator permissioning specification

```
Status:   Accepted
Created:  2018-10-02
Accepted: 2018-10-02
```

## Context

Validators are crucial part of unit-e. But if misbehaving - they can do a lot of harm. 
During initial deployment we would like to limit those who can be a validator.
This ADR introduces specification for permissioning subsystem.

## Decision

We define a whitelist of validators' public keys. Only whitelisted validators can send deposit and vote transactions.
All other validator transactions are not limited. I.e. validators can logout/withdraw even if they are not whitelisted.

Whitelist is stored in the blockchain. But not as a whole list - instead `admin transactions` carry
additions and removals from the list. So every node can reconstruct the entire list at any given time (block height).

Admin transactions are a special kind of transactions. They can be issued by whoever owns admin private keys.
To alleviate possible risk of losing one private key we also define a command that changes them. 

Initial admin keys will have to be hardcoded in chain parameters. Another option would be to hardcode them in the genesis block, however it creates some difficulties:
- Admin commands are placed in admin transactions, but genesis block usually contains only one transaction which is coinbase 
- Admin transactions should be signed. But there are no admin keys yet
- In a very rare case when we need to create a hardfork - this will be most likely done with chain parameters anyway

As mentioned above - permissioning is temporary. Once we decide to shut it down - we just issue the corresponding command. 
To summarize, we have 4 commands:
- Add validators to whitelist
- Remove validators from whitelist
- Reset administrators
- End permissioning

### Admin transaction requirements
- To quickly distinguish admin transactions from other we assign them their own `TxType = 7`
- They must spend something. This is to:
  - Be able to pay a fee for the entire transaction
  - Order admin transactions by chaining outputs of one into inputs of another
  - Confirm admin identity - see below
- Can have any number of inputs. But only the first one is _special_. It is used to confirm admin identity, so:
  - It must be segwit
  - It must use 2-of-3 multisignature
  - Witness must contain admin public keys
- Commands are stored in OP_RETURN outputs. One command - one output. Multiple commands in one transaction are allowed
- No OP_RETURN outputs are allowed except commands

All standard transaction validation rules are applied as well

### Commands format
Field         | Description                                  | Type/Size 
------------- | -------------------------------------------- | ----------------------
Command type  | One of the following command types:<br> `ADD_TO_WHITELIST = 0` <br> `REMOVE_FROM_WHITELIST = 1` <br> `RESET_ADMINS = 2` <br> `END_PERMISSIONING = 3` | uint8_t
Pubkeys #     | Number of pubkeys to follow                  | VarInt
Pubkeys       | Pubkeys                                      | variable

`RESET_ADMINS` command must contain exactly 3 public keys.

`END_PERMISSIONING` must not contain any.

`ADD_TO_WHITELIST` and `REMOVE_FROM_WHITELIST` must contain at least one.

All public keys should be valid and compressed.

### Permissioning end

After the `END_PERMISSIONING` command has been issued, new admin transactions should be rejected. Eventually the permissioning system will be removed. Admin commands from the past should be accepted/ignored. But rejecting new admin commands:
1) Helps to make post-permissioning implementation easier - after some block height just forbid admin transactions
2) Admin transactions remove some limitations on transaction outputs amount and size. To prevent anyone from sending such transactions and abusing the system we need to either keep admin validation or just forbid the whole thing

## Consequences

It is worth noting that admin commands are in effect only when they are included in block. More precise - starting from the next block. This happens because when appending a new block - we first check all transactions, and only then "process" them. 

Since commands are stored in the blockchain - they will stay there forever. Even after permissioning is over.
It is, however, possible to remove most of the code that processes them. In the end - they are _almost_ normal transactions.
