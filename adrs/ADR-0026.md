# ADR-26: Open the repos

```
Status:   Accepted
Created:  2019-04-09
Accepted: 2019-04-16
```

## Context

We run unit-e as an open source project. At the beginning of the project the git
repositories were kept private to the initial team in order to first get to a
state were it makes sense to get a broader audience involved. With the start of
the testnet, reflected in the [0.1
milestone](https://github.com/dtr-org/unit-e/milestone/11), we are reaching this
state. So we will open the initial set of repos and make them public on GitHub.

We have mostly worked on the repositories as if they would already be public, so
we should be in a good shape there, but it's still important to be clear about
what will be made public because it changes the visibility of our work and we
have a chance for a final review of what will be made public.

The purpose of this ADR is twofold:

First, it's meant to make it clear on which repositories we have agreed to make
public in the first step.

Second, it's supposed to get the awareness and buy-in from the whole team what
will be made public. So we can use the review process of this ADR to get the
approval of everybody that the repositories are good to be made public.

## Decision

We will make the following GitHub projects public on the date of the opening:

* https://github.com/dtr-org/unit-e
* https://github.com/dtr-org/uips
* https://github.com/dtr-org/unit-e-clonemachine
* https://github.com/dtr-org/docs.unit-e.io
* https://github.com/dtr-org/unit-e-project

The exact date of the opening is not subject of this ADR. This will be decided
by the team when everything is ready.

Each member of the team will approve this ADR to signal that they are fine with
opening the listed repositories, and that they are not aware of anything in
these repos which should not be published.

## Consequences

When this ADR is approved the listed repositories will be made public on GitHub
on the date of the opening.

An important consequence is that from that point on we work in the open and our
code and our discussions are publicly visible. This includes the complete
history of git, issues, and pull requests which is present in the GitHub
projects.

Opening the repos will make it possible to interact with a much bigger
community. We are then operating as a true open source project.

This also means that we need to make sure that the project is accessible from
outside of the initial team. There shouldn't be any internal context required to
understand what's going on in the project. This needs to be taken into account
when submitting pull requests and issues and commenting.

Being open also means that communication is becoming even more important as more
people are involved. Continuing our respectful and kind way to communicate will
be a great base there.
