# ADR-23: Unit-e improvement proposals (UIP)

```
Status:   Accepted
Created:  2018-11-29
Accepted: 2018-12-06
```

## Context

We use ADRs to keep track of decisions as described in
[ADR-1](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0001.md).
This is supposed to create a history of immutable records of decisions for
future reference.

We also need a place for discussing and agreeing on design questions, especially
on the protocol level. This also needs to record the context of which decisions
were taken, when, and why.

There needs to be a process for:

* discussing decisions
* taking decisions
* recording decisions
* updating decisions

It should be easy to reference decisions. If there are multiple versions of a
decision it needs to be clear which version is referenced.

Design decision documents should also be able to serve as specification.

We have used ADRs for both, recording decisions, including code and process
decisions and for having the protocol design discussions and decisions. This has
created some problems as it wasn't clear if documents should be updated or
replaced, the ADR template is not covering specific aspects of design decisions,
and it is mixing decisions of different domains which possibly also have a
different audience.

ADRs are also a good way to decide on a certain way of doing things such as "we
believe in open-source and gonna strive to open our repos as much as possible"
and demonstrate the team signing off on this. The protocol design process with
more complex status transitions and the need for review by experts on the
protocol level is not so suitable for this.

### Current ADRs

| ADR | Title | Status | Created | Accepted |
|---|---|:---:|:---:|:---:|
|[ADR-0001](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0001.md)|Adopt ADR|Accepted|2018-08-16|2018-08-17|
|[ADR-0002](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0002.md)|Define naming convention for actors in Esperanza|Accepted|2018-08-23|2018-08-24|
|[ADR-0003](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0003.md)|Unit-e Block Header to include SegWit Merkle Root|Accepted|2018-08-23|2018-09-04|
|[ADR-0004](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0004.md)|Unit-e Block Header NOT to include Kernel Hash|Accepted|2018-08-23|2018-09-04|
|[ADR-0006](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0006.md)|Adopt Google C++ Style Guide|Accepted|2018-08-23|2018-08-27|
|[ADR-0007](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0007.md)|Use genesis block for initial supply|Accepted|2018-08-30|2018-09-04|
|[ADR-0008](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0008.md)|Proper `headers` message|Accepted|2018-09-25|2018-09-25|
|[ADR-0009](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0009.md)|Validator permissioning specification|Accepted|2018-10-02|2018-10-02|
|[ADR-0011](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0011.md)|Snapshot|Accepted|2018-10-09|2018-11-06|
|[ADR-0012](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0012.md)|Fork choice rule|Accepted|2018-10-17|2018-10-25|
|[ADR-0016](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0016.md)|Adopt DCO|Accepted|2018-10-22|2018-11-06|
|[ADR-0017](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0017.md)|No Nonce or Extra Nonce|Accepted|2018-11-05|2018-11-03|
|[ADR-0018](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0018.md)|unit-e Transaction Types|Accepted|2018-11-02|
|ADR-10|Snapshot Verification|Proposed|
|ADR-15|Remote Staking|Proposed|
|ADR-21|Transfer Esperanza Transactions|Proposed|
|ADR-22|Coinstake Maturity|Proposed|
|ADR-19|Coin serialization per TX type|Retracted, converted to issue, not implemented|
|ADR-20|Propagate stake modifier using fast sync|Retracted, converted to issue, implemented|

The ADRs cover different domains:

* Protocol: 3, 8, 9, 11, 12, 17, 18, 10, 15, 21, 22, 20
* Process: 1, 16
* Code: 2, 4, 6, 7, 19


## Decision

* We split up the process for discussing design from recording decisions. For
  the first we create a new UIP (Unit-e Improvement Proposal) process, for the
  second we continue to use the ADR process. Protocol related design decisions
  fall under discussing design (in UIPs), process and code falls under recording
  decisions (as ADRs).
* ADRs are used for recording decisions. They result in a (generally) immutable
  record of decisions which are relevant on the development process or
  implementation and code level. This is the record of a decision at a given
  point in time. It can be revised by taking another decision which is recorded
  in a new ADR. ADR 1, 2, 4, 6, 7, 16, 19 represent this kind of decision
  records.
* UIPs are used for discussing and deciding design, especially related to
  protocol and API. They result in a design document which also serves as
  specification for the current protocol. These documents are mutable and
  reflect the current state of the design. ADR 3, 8, 9, 10, 11, 12, 17,
  18, 19, 20, 21, 22 represent this kind of design document.
* The UIP process is moved to a dedicated repository `dtr-org/uips` (which will
  be made public along with the other repositories).
* The protocol related ADRs which are in fact more design documents than
  decision records, as listed before, are moved as UIP to the
  `dtr-org/uips` repo. Their numbers will be kept.
* The UIP process will be documented in UIP-1. It will be based on the [BIP
  process](https://github.com/bitcoin/bips/blob/master/bip-0002.mediawiki). The
  exact details of how this process will work are out of scope of this ADR. This
  will be sorted out in UIP-1.
* For both processes:
  * The pull request review process is used for discussions of proposals, there
    might be a pre-discussion through other channels.
  * A summary of the discussion in the pull request should be added to the
    document before approving it.
  * Approving and merging the pull request means acceptance of the document as
    decision. The UIP process will define a more fine-grained set of decision
    levels to reflect states such as `Draft`, `Proposed`, `Final`. Exact
    definition of these states is out of scope of this ADR and will be defined
    as part of UIP-1.
  * When an accepted document is updated through another pull request which
    contains non-trivial changes, a changelog section is added.
  * Rejected proposals are not merged but kept in the pull request history, they
    are added to the table of content for reference.
* ADR-1 is updated to reflect the decisions of this ADR-23.

## Examples

### ADR as decision record

[ADR-16: Adopt DCO](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0016.md)
is a good example for the record of a decision about the development process.
There was a discussion in the [pull
request](https://github.com/dtr-org/unit-e-docs/pull/47) which resulted in the
whole team expressing approval for the decision. The ADR records that decision,
the context, rationale, when it was taken, and the consequences. The decision
was implemented in various changes in the different repositories such as
[documenting how to adhere to the DCO](https://github.com/dtr-org/unit-e/commit/3479899474cfbd57bb1d13768e6fe3704a1f8fe9#diff-6a3371457528722a734f3c51d9238c13).

### Design discussion (which will become a UIP)

[ADR-21: Transfer Esperanza
Transactions](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/ADR-0021.md)
is an example for a design document. There is a [draft
state](https://github.com/dtr-org/unit-e-docs/blob/5f4180223c6e6a5bfa13ab937cc9e30ef9d5941f/adrs/ADR-0021.md).
The [discussions](https://github.com/dtr-org/unit-e-docs/pull/59) resulted in a
new proposal which is discussed as an additional pull request which updates the
document.

Once approved this will move from Draft to Proposed. This should ultimately
happen in the dtr-org/uip repository once we have created it.

The document uses the ADR format which is not necessarily the best format for a
design document as context and consequences are not the main point but the specs
of the design. As UIP it will use a more design oriented format with more
fine-grained status.

## Consequences

* Protocol discussions will move to the UIPs in the new repository
  (`dtr-org/uips`).
* The UIP process needs to be written down.
* The ADR process needs to be updated
* When creating a new decision we will have to choose if to do that as ADR or
  UIP. This should be clear from the documentation.

The result should be more clarity in taking and recording decisions on all
levels, protocol, code, and process.
