# ADR-16: Adopt DCO

```
Status:   Accepted
Created:  2018-10-22
Accepted: 2018-11-06
```

## Context

For an open source project being able to distribute its code under the chosen
license it's important to make sure that all contributions are done under this
license and that contributors have the legal right to do so. There are three
ways how this is usually handled:

* Rely on the implicit agreement by contributors when they submit code to a
  project with a known license.
* Require contributors to sign a contributor license agreement (CLA) which
  explicitly assigns rights to the project and gives guarantees from the
  contributor. There are a variety of CLAs used by open source projects which
  differ in details such as what rights are given to the organization governing
  the project. For contributions being done by a company it's required that the
  company has signed a corporate CLA.
* The [Developer Certificate of Origin
  (DCO)](https://developercertificate.org/), established by the Linux
  Foundation, which is an explicit statement by contributors in each commit that
  they have the legal rights to contribute the code and are contributing the
  code under the license the project has chosen. This doesn't require signing
  formal documents between project and contributor or their employer.

There are two dimensions to consider in choosing which way to use, one is the
clarity about the terms of the contribution and the other is how much of a
barrier is created by adding requirements for contributions.

The DCO is an increasingly popular way of providing legal clarity while not
adding the overhead and barrier of a CLA. It works in a symmetric way, not
giving the project additional rights such as to relicense the code under a
proprietary license which often is the case in CLAs. It doesn't require signing
an agreement which can be difficult if the employer of the developer has to do
that. It is standardized and used by many open source projects such as the Linux
Kernel, Docker, Chef, or GitLab, so that many developers are already familiar
with it and know how to use it.

Using the DCO sends a clear signal that the open source project is serious about
the integrity of its code not only from a technical perspective but also from a
legal one.

## Decision

UnitE adopts the DCO. That means that all commits MUST be signed off by the
author by adding a statement at the end of the commit message in the form:

    Signed-off-by: Jane Doe <jd@example.com>

This statement declares that the author has the right to contribute the code and
does so under the license of the open source project, which in the case of UnitE
is MIT. The statement formally declares acceptance of the Developer Certificate
of Origin which is hosted at https://developercertificate.org/:

    Developer Certificate of Origin
    Version 1.1

    Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
    1 Letterman Drive
    Suite D4700
    San Francisco, CA, 94129

    Everyone is permitted to copy and distribute verbatim copies of this
    license document, but changing it is not allowed.


    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.

Other people involved with creating the submission, such as co-authors or the
committer, SHOULD add their own `Signed-off-by` statement so that you might get
multiple of these statements in a commit message.

## Consequences

### Being conscious and explicit about rights

Contributors need to make sure that they have the rights to contribute under the
terms of the project. While they generally have to do that in any case, making
it explicit increases the likelihood that they actually do it, for example
getting approval from their employer if necessary.

### Adding the sign-off statement

There is a bit of overhead when creating commits, because the `Signed-off-by`
statement needs to be added. The easiest way to do that is using the `-s` or
`--signoff` option of git when committing:

    git commit -s -m "My commit message"

This automatically adds the `Signed-off-by` statement using the name and email
the developer has configured in git. It still can be edited in the editor opened
by git along with the rest of the commit message.

Adding the statement can also be automated using a git hook. This requires
storing a script such as the following into the `.git/hooks` directory under the
name `prepare-commit-msg` and making this file executable.

```sh
#!/bin/sh

NAME=$(git config user.name)
EMAIL=$(git config user.email)

if [ -z "$NAME" ]; then
    echo "empty git config user.name"
    exit 1
fi

if [ -z "$EMAIL" ]; then
    echo "empty git config user.email"
    exit 1
fi

git interpret-trailers --if-exists doNothing --trailer \
    "Signed-off-by: $NAME <$EMAIL>" \
    --in-place "$1"
```

### Checking commits for sign-off message

To make sure that all commits are signed off and there is no code going into the
project without the confirmation of the DCO, commits have to be checked before
they are merged into the code base.

The simplest way to do that is to use the [DCO GitHub
App](https://github.com/probot/dco). This is a bot checking all commits in a
pull request and using GitHub's status checks to note results in the pull
request. By enabling required status checks in the GitHub project the DCO is
enforced on pull requests.

### Squashing commits

When using the squash-merge work flow in GitHub, the person doing the merge of
the pull request has to make sure that the sign-off messages of the commits are
preserved, and usually add their own message as well. As this is done in the
GitHub UI it adds a bit of manual work and needs some extra care.

### Documentation

The developer documentation in CONTRIBUTING.md needs to be updated with the DCO
instructions.
