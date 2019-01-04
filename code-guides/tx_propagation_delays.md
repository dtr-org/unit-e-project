# Transaction Propagation Delays

This write-up intends to share some knowledge on how transactions propagate and why it sometimes takes a lot of time.

## Inbound vs Outbound

Unlike other p2p technologies bitcoin separates `inbound` and `outbound` connections:

Outbound connection is initiated by the node itself. While inbound is initiated by someone else "from outside"

```
  Inbound   +-----+   Outbound
----------->| YOU |---------------->
            +-----+
```

The reason for this separation is security. An adversary can connect as `inbound` to almost any node. But it
can not force _you_ to connect to him.

This leads to a few peculiarities in how inbound and outbound data is handled.
We are going to concentrate on transaction propagation.

It is worth noting that data flows in both directions. I.e. nodes send transactions to both their inbound and outbound
peers.

## Diffusion and transaction delays

When bitcoin node decides to send a transaction to its neighbour - it never sends this transaction directly.
Instead, it puts the transaction into the buffer associated with this peer; then relays this buffer with some random
exponential intervals. This mechanism is called `diffusion`. It is intended to make it difficult for an adversary to
find the source of the transaction.

For `outbound` peers the relay interval is `Poisson(2)` seconds. For inbound peers it is `Poisson(5)` seconds.
Although on average those are 2 and 5 seconds respectively, in some cases this delay might be several minutes.

We can show this by looking at the underlying function from bitcoin:

```cpp
int64_t PoissonNextSend(int64_t nNow, int average_interval_seconds) {
    return nNow + (int64_t)(log1p(GetRand(1ULL << 48) * -0.0000000000000035527136788 /* -1/2^48 */) * average_interval_seconds * -1000000.0 + 0.5);
}
```

If we substitute output of random generator here with its maximum value we will get:

`max(Poisson(2)) =~ 59 seconds`

`max(Poisson(5)) =~ 148 seconds`

Note: You can roughly estimate maximum possible delay by multiplying Poisson argument by 30.

We often use functions like `wait_for_transaction` in functional tests. The above numbers mean that there is always a
small chance that this wait function fails (unless timeout is several minutes).

We now estimate this chance for some of the popular timeout values:

Timeout | Prob(Poisson(5) > Timeout) | Prob(Poisson(2) > Timeout)
--------|----------------------------|--------------------------
3s      |0.548812                    |0.22313
10s     |0.135335                    |0.00673795
15s     |0.0497871                   |0.000553085
30s     |0.00247875                  |3.05902e-07
60s     |6.14421e-06                 |0

Please note that those computations are only valid for a single connection. In a real world each node would have lots of
connections with lots of alternative routes between nodes, so overall propagation time will be different.

# Whitelisting

It is possible to completely disable diffusion for a selected node. Just add
it to the white list. In functional tests that can be achieved with
`-whitelist=127.0.0.1` extra argument.

## Simulations

To expand results on a slightly more complicated network topologies several simulations were run.
We start timer when node 0 sends a transaction. We stop timer when node 1 has this transaction in its mempool.
Below are recorded values for several small networks:

  &nbsp;| 0<->1 | 0->1 | 0<-1 | 0<->2<->1 | 0<->2<->1; 0<->3<->1 | 0<-1 + whitelist
--------|-------|------|------|-----------|-------------|-----------------
Average | 1.7   | 2.25 | 5    | 3.15      | 2.29        | 0.76
Min     | 0.48  | 1.46 | 0.47 | 0.49      | 0.56        | 0.59
Max     | 11.8  | 20.86| 40.1 | 14.25     | 8.59        | 1.03
Samples | 1000  | 1000 | 1000 | 501       | 3625        | 1000

Note: `0<->1` denotes bidirectional connection. Which is in fact two connections: inbound `0<-1` and outbound `0->1`.

Note: simulations were run on a local machine using functional tests framework.

[Raw data](https://docs.google.com/spreadsheets/d/1E5O0dCuLyzHj0BebIj1mpz3nh-rUEZ99TnzX6TYyGqM/edit?usp=sharing)

From the above table we can see that sends to an inbound node indeed take ~5 seconds, and ~2 seconds for outbound.
If a connection is bidirectional - transactions propagate even faster. Because they are being sent through both
inbound and outbound connections.

We can also clearly see alarmingly high maximum values in a networks with just 2 nodes. They decrease when more
alternative routes exist in the network. However be careful: maximum propagation time stays the same as the number of
alternative routes grows. It is the probability of getting it decreases.

## Recommendations to avoid flakiness in functional tests
- Use whitelisting to completely disable diffusion
- Prefer bidirectional connections
- Prefer fully-connected network topologies
- Avoid using `sleep` to wait for the transaction effects. You can use one of the special functions with timeouts instead:
  - `wait_for_transaction` - waits for specified transaction across all nodes in the test run
  - `sync_mempools` - waits until all of the passed nodes have equal mempools
  - `sync_blocks` - waits until all of the passed nodes have the same tip
  - `sync_all` - is a combination of `sync_mempools` and `sync_blocks`
  - `wait_until` - waits until a passed predicate is true
