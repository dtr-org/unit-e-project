# Description

This document should give an introduction and serve as a guideline in understanding the process of creating a transaction and committing it to the network.  
The process is explained trying to mediate between readability, completeness and relevance that lead into omitting some minor parts.

# Create transaction

The following is a detailed description of the steps at the moment utilized for creating a `STANDARD` non-witness transaction.  

```c++
CHDWallet::CreateTransaction(std::vector<CTempRecipient>& vecSend,
                              CWalletTx& wtxNew,
                              CReserveKey& reservekey,
                              CAmount& nFeeRet,
                              int& nChangePosInOut,
                              std::string& strFailReason,
                              const CCoinControl& coin_control,
                              bool sign
                            )
```

- `AddStandardInputs` - Add inputs and outputs
  - check that there are recipients
  - `InspectOutputs` - count the total output amount and check that is valid
  - `ExpandTempRecipients` - populates the scriptPubkey for the vector of recipients
  - `AvailableCoins` - return which coin are spendable from the wallet
    - for each element in the `mapWallet`:
    - `CheckFinalTx` - Check if the transaction is final in the sense of having lockTime in the past
    - checks in case of a coinstake that the coinMaturity is appropriate
    - for each standard output:
      - check if the coin is locked or spent
      - `IsMine` - check if the coin corresponding to the output is mine by looking at the key contained in the script
        - `Solver` - identifies the type of the script and returns it's solution (pubkey for most cases)
        - if the key corresponding to the solution is part of the wallet then return true, false otherwise
      - add the output to the coins to return
  - create a `CMutableTransaction` `txNew` representing the transaction to create and init it
  - Until successful (while true):
    - `SelectCoins` -  selects coins with the required amount
      - check if there are coin_control preset coins, if so add them to the result list
      - `SelectCoinsMinConf` - return the best fitting coin for the given amount randomly selecting from the ones available
    - if there is change set the change destination
      - create a tempRecipient for the change
      - `SetChangeDest` - selects the next key from the keypool
      - create a tempOutput with current scriptPubkey and change
      - check if the change remaining is so small that it should be added to the fees
      - `InsertChangeAddress` - insert the change output along with the other recipients
    - for each selected coin:
      - insert a new `CTxIn` in the `txNew.vin`
    - if the all the outputs are not standard then add a `CTxOutData` to `txNew.vpout`
    - for each recipient:
      - create and `CTxOutBase` of the right subtype with the given pubkey and amount
      - `CheckOutputValue` - check if the transaction is too small      
      - add the output to `txNew.vpout`
    - create a dummy signature of the transaction to estimate a fee value for the transaction
    - create `CTransaction txNewConst(txNew)`
    - `GetMinimumFee` - calculates the minimum fee given size, a feeEstimator and some constants
    - if the fee is more than needed try to select new coins to get closer with less excess fee
    - if the fee needed is actually more than the one given at the beginning then increase it using the change amount
    - if the previous step succeed break the loop, otherwise include more fee and continue from the beginning of the loop
  - if the sing input param was set then sign the transaction
    - `TransactionSignatureCreator` - initialize a sig creator
    - `ProduceSignature` - create a signature for the whole transaction
      - `SignStep`
        - `Solver` - solve the scriptPubKey if possible and return a solution for it (a pubkey usually)
        - `Sign1` - use the creator to create a signature
          - `TransactionSignatureCreator::CreateSig`
            - get the pubkey for a given address and keystore (wallet)
            - `SignatureHash` - return the sha256 of the serialized transaction
            - `Sign` - sing with ECDSA and serialize the signature data
      - `VerifyScript` - verify the script generated
        - `EvalScript` - run the scriptpubkey script with the scriptsig generated before
        - check that the stack contains TRUE at the end of the script execution
    - `UpdateTransaction` - add scriptsig and scriptwitness to `newTx`
    - there is a big chunk of logic run in case #ENABLE_USBDEVICE is set, here is not explained to maintain brevity and relevance
  - `PreAcceptMempoolTx` - check that the transaction is not too big (bytes) and that it passes ancestors/descendents limits



  # Commit transaction
  After creating the transaction (event though I believe that the steps above go a bit further than that), the next step is to broadcast it to the peers.

  ```c++
  bool CHDWallet::CommitTransaction(CWalletTx& wtxNew,
                                    CReserveKey& reservekey,
                                    CConnman* connman,
                                    CValidationState& state
                                  )
  ```

  - `AddToWallet`
    - create a `CWalletDB` that is nothing else but a wrapper for a DB transaction
    - if is not already there insert the input transaction into `mapWallet`
    - `AddToSpends` - add the input spent in this transaction to `mapTxSpent`
      - for each input:
        - add the `prevout` to the `mapTxSpent`
        - in case an equivalent element was already there then
        - SyncMetaData - copy fields from the new `prevout` to the one found
    - write the transaction to DB
    - break debit/credit balance caches
    - send a notification about a transaction being added to the wallet
    - broadcast a `MSG_HASHWTX` message
  - for each input of the committed transaction present in `mapWallet`:
    - `NotifyTransactionChanged` - mostly tells the transactiontablemodel to update the `prevout` transactions
  - `AcceptToMemoryPool` - run the full transaction validation, for brevity this method is explained separately later
  - `RelayWalletTransaction` -  broadcast a `MSG_TX` to peers

# Add to memory pool

```c++
bool CWalletTx::AcceptToMemoryPool(const CAmount& nAbsurdFee, CValidationState& state)
```

The above function is through some delegation calling the function below where most of the validation
of a transaction happens, this is the barrier for a transaction to be included in the mempool.

```c++
static bool AcceptToMemoryPoolWorker(const CChainParams& chainparams,
                                      CTxMemPool& pool,
                                      CValidationState& state,
                                      const CTransactionRef& ptx,
                                      bool* pfMissingInputs,
                                      int64_t nAcceptTime,
                                      std::list<CTransactionRef>* plTxnReplaced,
                                      bool bypass_limits,
                                      const CAmount& nAbsurdFee,
                                      std::vector<COutPoint>& coins_to_uncache
                                    )
```
  - `CheckTransaction`
    - check that the size of the transaction does not exceed `MAX_BLOCK_WEIGHT`
    - for each output `tx.vpout`:
      - `CheckStandardOutput`
        - `CheckValue` - check that the output amount is positive and < `MAX_MONEY`
    - `MoneyRange` check that the total amount of the transaction is > 0 and < `MAX_MONEY`
    - check that there are no duplicated outputs
    - check that the `prevouts` are not null
  - `IsStandardTx` - check `tx.vout` and `tx.pvout` to infer their type (a standard script is any normally accepted pay script see txnouttype in standard.h for more details)
  - `CheckFinalTx` - Check if the transaction is final in the sense of having lockTime in the past
  - check that the transaction is not already in the mempool
  - for each input `tx.vin`:
    - check if there is any conflicting `prevout` in `pool.mapNextTx` and save a set of them
  - check if there is any input we mentioned that we do not have in our local view and set `pfMissingInputs` accordingly
  - `CheckSequenceLocks` - only accepts transactions that can be mined in the next block
  - `Consensus::CheckTxInputs` - validates the inputs
    - for each `tx.vin`:
      - if is a coinbase check that is mature to be spent
      - check for negative or overflow values in the `prevout` amount
      - check that the fees are well formed and above the minimum expected fee for the transaction
  - `AreInputsStandard` - check that the scripts inside the input are not ill formed and very expensive to compute (to avoid a DoS)
  - `GetTransactionSigOpCost` - count how many operations does the `scriptPubKey`
  - check that this value is not > `MAX_STANDARD_TX_SIGOPS_COST` (16000)
  - create `CTxMemPoolEntry`
  - check fees > `mempoolRejectFee` and > `minRelayTxFee` and not incredibly high
  - `CalculateMemPoolAncestors` - check for parents and ancestors in the mempool and make sure that they are not too many or too big
  - check for spending of conflicting transactions intersecting ancestors and the conflicting set from before
  - handle replacements if any - the logic here is omitted for brevity cause is quite complex and handles different scenarios including transactions re-sent with different fees from the previous copy
  - `CheckInputs` - check whether all inputs of this transaction are valid (no double spends, scripts & sigs, amounts)
  - `CheckInputsFromMempoolAndCache` - check that no input is already spent and call `CheckInputs` again
  - remove conflicting transactions from the mempool
  - store transaction in memory (various caches)
  - add transaction to memory address index
  - add transaction to memory spent index
  - `LimitMempoolSize` - remove the transaction if expired
  - `AddKeyImagesToMempool` - add all the `tx.vin` pubkeys to the `mapKeyImages` of the pool
