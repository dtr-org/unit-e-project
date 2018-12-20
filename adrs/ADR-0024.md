# ADR-24: Define work flow and labels for issues

```
Status:   Proposal
Created:  2018-12-05
Accepted: 2018-12-20
```

## Context

We use [GitHub issues](https://guides.github.com/features/issues/) heavily for
all kinds of things, reporting bugs, requesting features, discussing ideas,
tracking work, recording failed tests, recording things to do, etc.

Pull requests technically are issues as well but GitHub treats them separately
in most parts of the UI.

Issues and pull requests share a set of labels, milestones, a search interface,
and a way to assign people.

Issues can also be used in [GitHub project
boards](https://help.github.com/articles/about-project-boards/) to have Kanban
style boards. This is useful to organize and track work and make priorities
clear.

Usually each repository has its own set of issues and pull requests but issues
can be disabled.

There are a few things in our work flow which are not well defined:

* Where do we track issues? Does each repo have its own issues or do we
  centralize some of them somewhere?
* How do we handle labels? What labels do we use? What do they mean? When are
  they assigned?
* How do we handle assignees? What does it mean to be assigned to an issue?

This ADR covers how we handle issues, labels, and assignees.

Milestones are out of scope of this ADR and will be decided separately because
they are more related to release and planning workflows than the data on
issues itself.

### Current labels

As context for a definition of labels see a [snapshot of the current
labels](files/ADR-0024/issue-labels-snapshot.md) in use as of 2018-12-4.


## Proposal

This is a proposal which is supposed to answer the open questions and create a
better definition of how we use issues and their labels. It's a starting point
and the idea is to decide on an initial definition, document that, and evolve
it over time through pull request on the documentation or further ADRs.

The documentation as it would look like according to the proposal is added in
the pull request as [issues.md](../project/issues.md). The ADR provides context
and rationale.

### Location of issues

Each repository has its own set of issues. They are not aggregated in one or
more central repositories.

*Rationale:* This keeps the issues close to the code and pull requests they
refer to. It makes it easier to get an overview of the issues for a specific
repository. It doesn't confuse people who only look at one repository and might
lack the context of other repos. Less labels are required per repository as
repo-specific labels only have to be in one.

### Assignees

The person working on an issue assigns themself to the issue. This shows that
there is active work the issue and who to talk to when others intend to work on
the same or related issues.

If there is no active work on an issue it should have no assignee. These issues
are up for grabs by anybody.

For pull requests the submitter of the pull request is usually the person
working on it. Having explicit assignees on pull requests is therefore optional.
If somebody else than the author is taking over the work on the pull request
they should add themself as assignee or ask a maintainer to add them.

### Titles

Titles of issues should be a short expressive description of what the issue is
about.

Issues are grouped by labels so they don't need prefixes such as `build:` or
`Feature`.

### Task lists

Use [task
lists](https://blog.github.com/2013-01-09-task-lists-in-gfm-issues-pulls-comments/)
in issues and pull requests to keep track of sub tasks which are too small to be
put into their own issue. This is a nice way to keep closely related things
together, have an indicator of progress, and get a good overview. The progress
is shown in issue lists in the GitHub UI.

### Labels

Labels represent information in different dimensions which are helpful to make
specific information about the issue more visible, to classify issues for easier
listing and filtering, and to assist with the workflow how issues are handled.

The following sections define types of labels in the different dimensions such
as status, type, or component. This includes a description of how each dimension
of labels is supposed to be used and a list of corresponding labels.

The list of labels is based on the current set of labels. It brings them into a
consistent format and defines what labels to add, change, and remove. This
represents a snapshot of the current labels as a starting point. Labels will be
maintained on GitHub. This ADR describes the general conventions for how to name
and structure them. Adding or changing individual labels in the future won't
require an ADR but can just be done in the GitHub UI. We'll look into automating
that so that there is a canonical version controlled definition of the labels in
git which can be discussed and changed via our usual development workflow.

Most labels are meant to be available across repositories while not all
repositories will have a need to use all of them. Not using a label is fine but
if a label is used it should fit into the overall definition.

Labels help with triaging incoming issues and preparing work to be done. Getting
a quick overview and being able to filter according to different categories is
essential. Labels also help with finding old issues and pull requests. So all
issues and pull request should be labeled accordingly.

Assigning labels should help with the process and not become an exercise for the
sake of assigning labels.

Colors of labels can be used to group them (see for example [how Robin does
it](https://robinpowered.com/blog/best-practice-system-for-organizing-and-tagging-github-issues/)).

#### General conventions

Spelling of labels is all lower-case. Words are separated by spaces.

If a label is split in several sub-labels they are indicated by a colon such as
`test: broken`, `test: floating`. This keeps them sorted together in the lists
for selecting labels for assignment or filtering.

#### Status

These labels indicate a certain status in the workflow. This adds more
fine-grained status information to the status which already is handled by the
GitHub UI (open, closed, review status of pull requests).

##### Pull request status

* `backport to bitcoin`: Changes which are supposed to be contributed
  upstream
* `backported to bitcoin`: Changes which successfully have been contributed
  upstream
* `wip` (was: `WIP`): Work in progress which is not supposed to be merged yet

##### Issue status

* `needs design`: Needs a design (possibly in a UIP) before it can be
  implemented
* `waiting: feedback` (new): Waiting for feedback

##### To be removed

* `wontfix`, `duplicate`, `invalid` (these only make sense for closed issues,
  there the comment should say why it's closed in a nice way, then they are out
  of sight and out of mind)
* `has ADR` (ADRs can be linked in the issue itself)

#### Type

This indicates the type of the issue. Each issue MUST have exactly one type.
Issues of the same type should be similar in content, format, and process.

* `bug`: A problem of existing functionality
* `feature` (was `enhancement`): New functionality
* `refactoring`: Changes which clean up code but don't change the user-visible
  behavior
* `performance`: Affecting the performance of the software
* `tests: broken` (was `broken test`): A broken automated test
* `tests: floating` (was `floating test`): An automated test which occasionally
  fails

##### To be removed

* `question` (not used)
* `trivial` (nothing is trivial in software)

#### Category

These labels indicate a general category. It's usually not tied to a specific
part of the code. It can help with grouping issues together, for example on a
project board, or when filtering work done by specific people or in a specific
way (e.g. security issues).

Issues can have zero, one, or multiple categories.

* `repo`: Configuration of the repository itself
* `build`: Build system
* `tests`: Automated tests
* `style` (was: `code style and naming`): Code style and naming
* `documentation`: Documentation
* `security`: Security-related issues
* `technical debt`: Cleaning up code which is there for historical reasons
* `tools`: Development tools
* `usability`: Issues with the user experience as an end user
* `open sourcing`: Task related to setting up the open source project
* `process`: About the way we work
* `compatibility`: Everything related with compatibility issues
* `upstream sync`: Related to upstream merges (clonemachine issues won't need
  this label anymore because they are moved to the clonemachine repo)
* `ci` (was: `travis`): Continuous integration

##### To be removed

* `utils/logs` (there is `tools`)

#### Component

These labels indicate a specific part of the code. It might also indicate that
special domain knowledge is required to work on these issues.

Issues can have be assigned to zero, one, or multiple components.

These labels are specific per repository.

##### unit-e

* `consensus`
* `economics`
* `finalization`
* `genesis`
* `p2p` (was: `P2P`)
* `permissioning`
* `policy`
* `privacy`
* `proposing`
* `rpc` (was: `RPC`)
* `utxo db and indexes` (was: `UTXO Db and Indexes`)
* `wallet`

##### unit-e-docs

* `adr` (was: decision): Decision record
* `docs`: General documentation
* `docs: user`: End user documentation
* `docs: operator`: Operator documentation
* `docs: developer`: Developer documentation

#### Welcome issues

It has become a good practice to indicate issues which are a good starting point
for new people. There are several conventions used for that. We settle on one
which is natively supported by GitHub.

* `good first issue`: Good issue to start with as somebody new to the project

##### To be removed

* `help wanted` (redundant)

#### Platform

This is used for flagging platform specific issues.

* `platform: linux` (was: `Linux/Unix`)
* `platform: mac` (was: `macOS`)
* `platform: windows` (was: `Windows`)
* `platform: freebsd` (new)


## Decision

* Adopt the proposal as defined in the section [Proposal](#proposal).
* Document the definition of how to handle issues in
  `dtr-org/unit-e-docs/project/issues.md`


## Consequences

* Documentation has to be added
* Some labels will have to be renamed, removed, and added
* Label descriptions have to be added
* For a few labels the prefix in the title has to be replaced by a label
* Clonemachine issues have to be enabled and the clonemachine-related issues
  have to be moved from the unit-e repo to the clonemachine repo
* Mergeable configuration has to be adapted

The result of all this should be a clearer, more consistent, and easier to
understand view on issues.

Most of it should eventually be obvious from the way how it's used so that the
documentation serves as a reference and definition but is not required for the
daily work.


## References

There is a bit of documentation, good material about issues, and examples of
projects which use it in a good way. Here are some references:

* http://issuelabeling.com has some good general guidelines
* Examples for good descriptions of labels:
  * https://docs.readthedocs.io/en/latest/issue-labels.html
  * https://github.com/electron/electron/labels
* Documentation how GitHub uses labels to help new people:
  https://help.github.com/articles/helping-new-contributors-find-your-project-with-labels/
* Tools:
  * [Labeler](https://github.com/tonglil/labeler), a tool to manage labels from
    a YAML file. It's not completely up to date with the GitHub API so it
    doesn't support descriptions and it has a few missing features such as being
    able to manage labels across repositories.
  * [GitHub Provider for
    Terraform](https://www.terraform.io/docs/providers/github/index.html)
