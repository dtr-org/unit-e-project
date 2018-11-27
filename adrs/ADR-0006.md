# ADR-6: Adopt Google C++ Style Guide

```
Status:   Accepted
Created:  2018-08-23
Accepted: 2018-08-27
```

## Context

The bitcoin-core source code does not follow a coherent code style. We feel that a coherent
code style is beneficial for readability and thus for maintenance as well as reviewing patches,
etc.

There are several accepted C++ styles out there. This ADR proposes to adopt the [Google
C++ Style Guide](https://google.github.io/styleguide/cppguide.html).

### Discussion

#### Pros

- code is readable
- nobody is faced with the question "how should I format this?"
- patches that merely format anything just do not happen
- changesets should be less big and concentrate on the actual changes
- adopting an existing style guide enables us to simply link to it
- adopting an existing style guide enables us to use predefined config for `clang-format`, `CLion`, etc.
- adopting an existing style makes it more likely for new people to already know it

#### Cons

- the existing code style might look like shit here and there (which is subjective and [touches people's sense of beauty](https://www.youtube.com/watch?v=HCXd3hJsBHk))

## Decision

We will adopt the following process:

* Code that is merged into unit-e/master MUST be formatted using the Google C++ Style

## Consequences 

Adopting a coherent code style and formatting the codebase in this coheren codebase
is a simple, mechanical task. However, since formatting touches almost every line,
it will make it harder to discover the git history of features (git blame will show
the author of the formatting commit for almost every line).

Merging upstream changes from bitcoin into unit-e will require us to make formatting
part of the [clonemachine](https://github.com/dtr-org/clonemachine). The process for
merging with bitcoin upstream is:

- fetch bitcoin branch into your repository
- apply clonemachine
- you know have a fresh, clean fork of bitcoin which looks and quacks a bit like unit-e
- merge unit-e master with your integration-branch (with the clean fork)

Follow-up tasks:

- integrate `clang-format` into the clonemachine
- retroactively apply google format on the current unite-master (actually, running the clone machine should be idempotent, maybe try that!)

