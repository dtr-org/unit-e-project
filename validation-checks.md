# Validation Checks

Bitcoin, Particl, and unit-e feature different checks in validation. Some of them consensus critical,
some of them to detect DoS attacks early, etc.

# [bitcoin 0.16](https://github.com/bitcoin/bitcoin/tree/0.16)

## `CheckBlockHeader`

### `high-hash` / proof of work failed

[validation.cpp:2985](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L2985)

```C++
static bool CheckBlockHeader(const CBlockHeader& block, CValidationState& state, const Consensus::Params& consensusParams, bool fCheckPOW = true)
{
    // Check proof of work matches claimed amount
    if (fCheckPOW && !CheckProofOfWork(block.GetHash(), block.nBits, consensusParams))
        return state.DoS(50, false, REJECT_INVALID, "high-hash", false, "proof of work failed");

    return true;
}
```

## `CheckBlock`

### `bad-txnmrklroot` / hashMerkleRoot mismatch

[validation.cpp:3007](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3007)

```C++
bool mutated;
uint256 hashMerkleRoot2 = BlockMerkleRoot(block, &mutated);
if (block.hashMerkleRoot != hashMerkleRoot2)
    return state.DoS(100, false, REJECT_INVALID, "bad-txnmrklroot", true, "hashMerkleRoot mismatch");
```

### `bad-txns-duplicate` / duplicate transaction

[BIP98: Fast Merkle Trees](https://github.com/bitcoin/bips/blob/master/bip-0098.mediawiki)

[validation.cpp:3013](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3013)

```C++
// Check for merkle tree malleability (CVE-2012-2459): repeating sequences
// of transactions in a block without affecting the merkle root of a block,
// while still invalidating it.
if (mutated)
    return state.DoS(100, false, REJECT_INVALID, "bad-txns-duplicate", true, "duplicate transaction");
```

### `bad-blk-length` / size limits failed

[validation.cpp:3024](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3024)

```C++
if (block.vtx.empty() || block.vtx.size() * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT || ::GetSerializeSize(block, SER_NETWORK, PROTOCOL_VERSION | SERIALIZE_TRANSACTION_NO_WITNESS) * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT)
    return state.DoS(100, false, REJECT_INVALID, "bad-blk-length", false, "size limits failed");
```

### `bad-cb-missing` / first tx is not coinbase

[validation.cpp:3028](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3028)

```C++
if (block.vtx.empty() || !block.vtx[0]->IsCoinBase())
    return state.DoS(100, false, REJECT_INVALID, "bad-cb-missing", false, "first tx is not coinbase");
```

### `bad-cd-multiple` / more than one coinbase

[validation.cpp:3031](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3031)

```C++
for (unsigned int i = 1; i < block.vtx.size(); i++)
    if (block.vtx[i]->IsCoinBase())
        return state.DoS(100, false, REJECT_INVALID, "bad-cb-multiple", false, "more than one coinbase");
```

### Check transactions

[validation.cpp:3033](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3033)

```C++
for (const auto& tx : block.vtx)
    if (!CheckTransaction(*tx, state, true))
        return state.Invalid(false, state.GetRejectCode(), state.GetRejectReason(),
                             strprintf("Transaction check failed (tx hash %s) %s", tx->GetHash().ToString(), state.GetDebugMessage()));
```

### `bad-blk-sigops` / out-of-bounds SigOpCount

[validation.cpp:3045](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3045)

```C++
if (nSigOps * WITNESS_SCALE_FACTOR > MAX_BLOCK_SIGOPS_COST)
    return state.DoS(100, false, REJECT_INVALID, "bad-blk-sigops", false, "out-of-bounds SigOpCount");
```


## `ContextualCheckBlockHeader`

### `bad-diffbits` / incorrect proof of work

This checks the Proof-of-Work requirement in the context of the current
and the previous block, and whether the difficulty was correctly accounted
for. While unit-e has a similar difficulty adjustment, it does not have
Proof-of-Work and so this particular check was removed from the codebase.

The pull request which removed it is [#612](https://github.com/dtr-org/unit-e/pull/612),
the commit on master is [1aecc28b](https://github.com/dtr-org/unit-e/commit/1aecc28bf37bfa3a3651cc5645d14a503f7080b0).

[validation.cpp:3132](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3132)

```C++
const Consensus::Params& consensusParams = params.GetConsensus();
if (block.nBits != GetNextWorkRequired(pindexPrev, &block, consensusParams))
    return state.DoS(100, false, REJECT_INVALID, "bad-diffbits", false, "incorrect proof of work");
```

### `bad-fork-prior-to-checkpoint` / `fCheckpointsEnabled`

[validation.cpp:3141](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3141)

```C++
if (fCheckpointsEnabled) {
    // Don't accept any forks from the main chain prior to last checkpoint.
    // GetLastCheckpoint finds the last checkpoint in MapCheckpoints that's in our
    // MapBlockIndex.
    CBlockIndex* pcheckpoint = Checkpoints::GetLastCheckpoint(params.Checkpoints());
    if (pcheckpoint && nHeight < pcheckpoint->nHeight)
        return state.DoS(100, error("%s: forked chain older than last checkpoint (height %d)", __func__, nHeight), REJECT_CHECKPOINT, "bad-fork-prior-to-checkpoint");
}
```

### `time-too-old` / block's timestamp is too early

[validation.cpp:3146](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3146)

```C++
if (block.GetBlockTime() <= pindexPrev->GetMedianTimePast())
    return state.Invalid(false, REJECT_INVALID, "time-too-old", "block's timestamp is too early");
```

### `time-too-new` / block timestamp too far in the future

[validation.cpp:3150](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3150)

```C++
if (block.GetBlockTime() > nAdjustedTime + MAX_FUTURE_BLOCK_TIME)
    return state.Invalid(false, REJECT_INVALID, "time-too-new", "block timestamp too far in the future");
```

### `REJECT_OBSOLETE` / version number check for pre-bip9 softforks

These checks are not relevant for `unit-e` as we removed the softforks and
respective bip versions for these pre-bip9 deployed softforks. They are
enabled by default and enforced for all blocks since (including) the genesis
block.

[validation.cpp:3154](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3154)

```C++
if((block.nVersion < 2 && nHeight >= consensusParams.BIP34Height) ||
   (block.nVersion < 3 && nHeight >= consensusParams.BIP66Height) ||
   (block.nVersion < 4 && nHeight >= consensusParams.BIP65Height))
        return state.Invalid(false, REJECT_OBSOLETE, strprintf("bad-version(0x%08x)", block.nVersion),
                             strprintf("rejected nVersion=0x%08x block", block.nVersion));
```

## `ContextualCheckBlock`

### `bad-txns-nonfinal` / non-final transaction

[validation.cpp:3186](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3186)

```C++
for (const auto& tx : block.vtx) {
    if (!IsFinalTx(*tx, nHeight, nLockTimeCutoff)) {
        return state.DoS(10, false, REJECT_INVALID, "bad-txns-nonfinal", false, "non-final transaction");
    }
}
```

### `bad-cb-height` / block height mismatch in coinbase

[validation.cpp:3196](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3196)

```C++
if (nHeight >= consensusParams.BIP34Height)
{
    CScript expect = CScript() << nHeight;
    if (block.vtx[0]->vin[0].scriptSig.size() < expect.size() ||
        !std::equal(expect.begin(), expect.end(), block.vtx[0]->vin[0].scriptSig.begin())) {
        return state.DoS(100, false, REJECT_INVALID, "bad-cb-height", false, "block height mismatch in coinbase");
    }
}
```

### `bad-witness-nonce-size` / invalid witness nonce size

[validation.cpp:3218](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3218)

```C++
bool malleated = false;
uint256 hashWitness = BlockWitnessMerkleRoot(block, &malleated);
// The malleation check is ignored; as the transaction tree itself
// already does not permit it, it is impossible to trigger in the
// witness tree.
if (block.vtx[0]->vin[0].scriptWitness.stack.size() != 1 || block.vtx[0]->vin[0].scriptWitness.stack[0].size() != 32) {
    return state.DoS(100, false, REJECT_INVALID, "bad-witness-nonce-size", true, strprintf("%s : invalid witness nonce size", __func__));
}
```

### `bad-witness-merkle-match` / witness merkle commitment mismatch

[validation.cpp:3222](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3222)

```C++
CHash256().Write(hashWitness.begin(), 32).Write(&block.vtx[0]->vin[0].scriptWitness.stack[0][0], 32).Finalize(hashWitness.begin());
if (memcmp(hashWitness.begin(), &block.vtx[0]->vout[commitpos].scriptPubKey[6], 32)) {
    return state.DoS(100, false, REJECT_INVALID, "bad-witness-merkle-match", true, strprintf("%s : witness merkle commitment mismatch", __func__));
}
```

### `unexpected-witness` / unexpected witness data found

[validation.cpp:3232](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3232)

```C++
if (!fHaveWitness) {
  for (const auto& tx : block.vtx) {
        if (tx->HasWitness()) {
            return state.DoS(100, false, REJECT_INVALID, "unexpected-witness", true, strprintf("%s : unexpected witness data found", __func__));
        }
    }
}
```

### `bad-blk-weight` / weight limit failed

[validation.cpp:3244](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3244)

```C++
if (GetBlockWeight(block) > MAX_BLOCK_WEIGHT) {
    return state.DoS(100, false, REJECT_INVALID, "bad-blk-weight", false, strprintf("%s : weight limit failed", __func__));
}
```


## `AcceptBlockHeader`

### `duplicate` / block is marked invalid

[validation.cpp:3265](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3265)

```C++
if (pindex->nStatus & BLOCK_FAILED_MASK)
    return state.Invalid(error("%s: block %s is marked invalid", __func__, hash.ToString()), 0, "duplicate");
```

### `prev-blk-not-found` / prev block not found

[validation.cpp:3276](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3276)

```C++
BlockMap::iterator mi = mapBlockIndex.find(block.hashPrevBlock);
if (mi == mapBlockIndex.end())
    return state.DoS(10, error("%s: prev block not found", __func__), 0, "prev-blk-not-found");
```

### `bad-prevblk` / prev block invalid

[validation.cpp:3279](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3279)

```C++
if (pindexPrev->nStatus & BLOCK_FAILED_MASK)
    return state.DoS(100, error("%s: prev block invalid", __func__), REJECT_INVALID, "bad-prevblk");
```

[validation.cpp:3293](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L3293)

```C++
if (!pindexPrev->IsValid(BLOCK_VALID_SCRIPTS)) {
    for (const CBlockIndex* failedit : g_failed_blocks) {
        if (pindexPrev->GetAncestor(failedit->nHeight) == failedit) {
            assert(failedit->nStatus & BLOCK_FAILED_VALID);
            CBlockIndex* invalid_walk = pindexPrev;
            while (invalid_walk != failedit) {
                invalid_walk->nStatus |= BLOCK_FAILED_CHILD;
                setDirtyBlockIndex.insert(invalid_walk);
                invalid_walk = invalid_walk->pprev;
            }
            return state.DoS(100, error("%s: prev block invalid", __func__), REJECT_INVALID, "bad-prevblk");
        }
    }
}
```

## `ConnectBlock`

We try to touch `ConnectBlock` as little as possible and it's not going to be substituted
in the foreseeable future.

### `bad-txns-BIP30` / tried to overwrite transaction

This [has been removed](https://github.com/dtr-org/unit-e/commit/a8afc6c#diff-24efdb00bfbe56b140fb006b562cc70bL1937)
from `unit-e` as it was superfluos with `BIP-34` enabled by default.

[validation.cpp:1884](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L1884)

```C++
if (fEnforceBIP30) {
    for (const auto& tx : block.vtx) {
        for (size_t o = 0; o < tx->vout.size(); o++) {
            if (view.HaveCoin(COutPoint(tx->GetHash(), o))) {
                return state.DoS(100, error("ConnectBlock(): tried to overwrite transaction"),
                                 REJECT_INVALID, "bad-txns-BIP30");
            }
        }
    }
}
```

### `bad-txns-accumulated-fee-outofrange` / accumulated fee in the block out of range

[validation.cpp:1928](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L1928)

```C++
if (!MoneyRange(nFees)) {
    return state.DoS(100, error("%s: accumulated fee in the block out of range.", __func__),
                     REJECT_INVALID, "bad-txns-accumulated-fee-outofrange");
}
```

### `bad-txns-nonfinal` / contains a non BIP68-final transaction

[validation.cpp:1941](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L1941)

```C++
if (!SequenceLocks(tx, nLockTimeFlags, &prevheights, *pindex)) {
    return state.DoS(100, error("%s: contains a non-BIP68-final transaction", __func__),
                     REJECT_INVALID, "bad-txns-nonfinal");
}
```

### `bad-blk-sigops` / too many sigops

[validation.cpp:1952](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L1952)

```C++

// GetTransactionSigOpCost counts 3 types of sigops:
// * legacy (always)
// * p2sh (when P2SH enabled in flags and excludes coinbase)
// * witness (when witness enabled in flags and excludes coinbase)
nSigOpsCost += GetTransactionSigOpCost(tx, view, flags);
if (nSigOpsCost > MAX_BLOCK_SIGOPS_COST)
    return state.DoS(100, error("ConnectBlock(): too many sigops"),
                     REJECT_INVALID, "bad-blk-sigops");
```

### `bad-cb-amount` / coinbase pays too much

[validation.cpp:1979](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L1979)

```C++
CAmount blockReward = nFees + GetBlockSubsidy(pindex->nHeight, chainparams.GetConsensus());
if (block.vtx[0]->GetValueOut() > blockReward)
    return state.DoS(100,
                     error("ConnectBlock(): coinbase pays too much (actual=%d vs limit=%d)",
                           block.vtx[0]->GetValueOut(), blockReward),
                           REJECT_INVALID, "bad-cb-amount");
```

### `block-validation-failed` / script verification

[validation.cpp:1982](https://github.com/bitcoin/bitcoin/blob/0.16/src/validation.cpp#L1982)

```C++
if (!control.Wait())
    return state.DoS(100, error("%s: CheckQueue failed", __func__), REJECT_INVALID, "block-validation-failed");
```

See [script_error.cpp](https://github.com/bitcoin/bitcoin/blob/0.16/src/script/script_error.cpp)
for a list of possible script errors.

# `tx_verify.cpp`

## `CheckTransaction`

The only conceptual change which will be done with respect to `CheckTransaction` is that the coinbase
transaction is checked as part of `BlockValidator::CheckBlock`, separately from other transactions.
This function will be invoked only for transactions of `TxType::STANDARD`, not any other (also not
`TxType::COINBASE` therefore). It is thus not necessary to change anything in here (though we could
get rid of the `if (tx.IsCoinBase())` branch).

```C++
bool CheckTransaction(const CTransaction& tx, CValidationState &state, bool fCheckDuplicateInputs)
{
    // Basic checks that don't depend on any context
    if (tx.vin.empty())
        return state.DoS(10, false, REJECT_INVALID, "bad-txns-vin-empty");
    if (tx.vout.empty())
        return state.DoS(10, false, REJECT_INVALID, "bad-txns-vout-empty");
    // Size limits (this doesn't take the witness into account, as that hasn't been checked for malleability)
    if (::GetSerializeSize(tx, SER_NETWORK, PROTOCOL_VERSION | SERIALIZE_TRANSACTION_NO_WITNESS) * WITNESS_SCALE_FACTOR > MAX_BLOCK_WEIGHT)
        return state.DoS(100, false, REJECT_INVALID, "bad-txns-oversize");

    // Check for negative or overflow output values
    CAmount nValueOut = 0;
    for (const auto& txout : tx.vout)
    {
        if (txout.nValue < 0)
            return state.DoS(100, false, REJECT_INVALID, "bad-txns-vout-negative");
        if (txout.nValue > MAX_MONEY)
            return state.DoS(100, false, REJECT_INVALID, "bad-txns-vout-toolarge");
        nValueOut += txout.nValue;
        if (!MoneyRange(nValueOut))
            return state.DoS(100, false, REJECT_INVALID, "bad-txns-txouttotal-toolarge");
    }

    // Check for duplicate inputs - note that this check is slow so we skip it in CheckBlock
    if (fCheckDuplicateInputs) {
        std::set<COutPoint> vInOutPoints;
        for (const auto& txin : tx.vin)
        {
            if (!vInOutPoints.insert(txin.prevout).second)
                return state.DoS(100, false, REJECT_INVALID, "bad-txns-inputs-duplicate");
        }
    }

    if (tx.IsCoinBase())
    {
        if (tx.vin[0].scriptSig.size() < 2 || tx.vin[0].scriptSig.size() > 100)
            return state.DoS(100, false, REJECT_INVALID, "bad-cb-length");
    }
    else
    {
        for (const auto& txin : tx.vin)
            if (txin.prevout.IsNull())
                return state.DoS(10, false, REJECT_INVALID, "bad-txns-prevout-null");
    }

    return true;
}
``` 

## `CheckTxInputs`

This function is not to be touched in `unit-e` at all.

```C++
bool Consensus::CheckTxInputs(const CTransaction& tx, CValidationState& state, const CCoinsViewCache& inputs, int nSpendHeight, CAmount& txfee)
{
    // are the actual inputs available?
    if (!inputs.HaveInputs(tx)) {
        return state.DoS(100, false, REJECT_INVALID, "bad-txns-inputs-missingorspent", false,
                         strprintf("%s: inputs missing/spent", __func__));
    }

    CAmount nValueIn = 0;
    for (unsigned int i = 0; i < tx.vin.size(); ++i) {
        const COutPoint &prevout = tx.vin[i].prevout;
        const Coin& coin = inputs.AccessCoin(prevout);
        assert(!coin.IsSpent());

        // If prev is coinbase, check that it's matured
        if (coin.IsCoinBase() && nSpendHeight - coin.nHeight < COINBASE_MATURITY) {
            return state.Invalid(false,
                REJECT_INVALID, "bad-txns-premature-spend-of-coinbase",
                strprintf("tried to spend coinbase at depth %d", nSpendHeight - coin.nHeight));
        }

        // Check for negative or overflow input values
        nValueIn += coin.out.nValue;
        if (!MoneyRange(coin.out.nValue) || !MoneyRange(nValueIn)) {
            return state.DoS(100, false, REJECT_INVALID, "bad-txns-inputvalues-outofrange");
        }
    }

    const CAmount value_out = tx.GetValueOut();
    if (nValueIn < value_out) {
        return state.DoS(100, false, REJECT_INVALID, "bad-txns-in-belowout", false,
            strprintf("value in (%s) < value out (%s)", FormatMoney(nValueIn), FormatMoney(value_out)));
    }

    // Tally transaction fees
    const CAmount txfee_aux = nValueIn - value_out;
    if (!MoneyRange(txfee_aux)) {
        return state.DoS(100, false, REJECT_INVALID, "bad-txns-fee-outofrange");
    }

    txfee = txfee_aux;
    return true;
}
```