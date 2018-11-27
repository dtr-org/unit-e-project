# ADR-8 Proper `headers` message

```
Status:   Approved
Created:  2018-09-25
Accepted: 2018-09-25
```

## Context

Nodes exchange blocks using various message. Ever since the _headers first_ approach was
introduced, nodes ask for headers first. They do so by issuing a `getheaders` message which
enumerates a list of block hashes and receive a `headers` message in return. The headers
message is simply a compact integer denoting the number of headers contained in the message
and the serialized block headers.

In bitcoin these headers are serialized as if they were blocks, but stripped from the
transactions. A block contains a compact integer that denotes the number of transactions
following. As the `headers` message does not contain transactions this number is always
zero, denoted by the single byte `0x00`.

This byte is superfluous.

The one and only place where headers are sent in bitcoin looks like this:

```C++
// we must use CBlocks, as CBlockHeaders won't include the 0x00 nTx count at the end
std::vector<CBlock> vHeaders;
int nLimit = MAX_HEADERS_RESULTS;
// ... omitted for brevity (logging) ...
for (; pindex; pindex = chainActive.Next(pindex))
{
    vHeaders.push_back(pindex->GetBlockHeader());
    if (--nLimit <= 0 || pindex->GetBlockHash() == hashStop)
        break;
}
// ... omitted for brevity (comment) ...
connman->PushMessage(pfrom, msgMaker.Make(NetMsgType::HEADERS, vHeaders));
```

The one and only place where the `headers` message is processed looks like this:

```C++
unsigned int nCount = ReadCompactSize(vRecv);
// ... omitted for brevity (length check) ...
headers.resize(nCount);
for (unsigned int n = 0; n < nCount; n++) {
    vRecv >> headers[n];
    ReadCompactSize(vRecv); // ignore tx count; assume it is 0.
}
```

As can be seen, the deserialization simply assumes that this byte will always be
zero and skips (ignores) it. The serialization can be changed to actually serialize
a `CBlockHeader`.

This was uncovered when adding the Proof-of-Stake block signature to a block, as the above
serialization code will unnecessarily serialize that into the headers message, too.

An alternative approach would be to define a `NotSoCompactHeaders` class which serializes
into the old headers message.

## Decision

We will serialize actual headers and not include the `0x00` byte in the end of the
`headers` message.

## Consequences

The headers message could be interpreted like a Block (obviously the computation of the
merkle tree for the transactions would fail) which might be handy for SPV clients.

There are tests that need to change. This is easily accomplished by changing the
`msg_headers` function:

```python
# headers message has
# <count> <vector of block headers>
class msg_headers():
    command = b"headers"

    def deserialize(self, f):
        # comment in united indicates these should be deserialized as blocks
        blocks = deser_vector(f, CBlock)
        for x in blocks:
            self.headers.append(CBlockHeader(x))
# ...
```

## Comments

Andrew:

> I believe it is just a historical thing, I don't know of any block parsing code that's really relevant where this is a problem and hard to change
> 
> I'd approve removing it, possibly making a list of things that depend on the difference and checking if theres test coverage for it

Peter Wuille (comments on bitcoin.stackexchange): https://bitcoin.stackexchange.com/a/36134/83940

Another thread on bitcoin.stackexchange asking precisely about the `txn_count` being always zero: https://bitcoin.stackexchange.com/q/2104/83940
