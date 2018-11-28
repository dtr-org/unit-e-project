# ADR-4: Unit-e Block Header NOT to include Kernel Hash

```
Status:   Accepted
Created:  2018-08-23
Accepted: 2018-09-04
```

## Context

Putting the *kernel hash* into the Block Header of Unit-E was
(proposed)[https://github.com/dtr-org/unit-e/issues/14]. Thinking
about it revealed that it does not help us.

## Decision

We will not make the kernel hash or stake modifier part of the block header.

## Consequences

None. We just don't do it.
