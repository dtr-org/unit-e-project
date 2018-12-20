# Conventions for GitHub issues

This document describes the conventions for issue tracking we use across the
repositories related to Unit-e. See [ADR-24](../adrs/ADR-0024.md) for some
background and rationale.

## Location of issues

Each repository has its own set of issues for issues related to the content of
the repository. For more general issues which can't be assigned to a specific
repository you can use the [`dtr-org/unit-e-docs`
issues](https://github.com/dtr-org/unit-e-docs/issues).

## Assignees

The person working on an issue assigns themself to the issue. This shows that
there is active work the issue and who to talk to when others intend to work on
the same or related issues.

If there is no active work on an issue it should have no assignee. These issues
are up for grabs by anybody.

For pull requests the submitter of the pull request is usually the person
working on it. Having explicit assignees on pull requests is therefore optional.
If somebody else than the author is taking over the work on the pull request
they should add themself as assignee or ask a maintainer to add them.

## Titles

Titles of issues should be a short expressive description of what the issue is
about.

Issues are grouped by labels so you don't need to add a prefix.

## Task lists

Use [task
lists](https://blog.github.com/2013-01-09-task-lists-in-gfm-issues-pulls-comments/)
in issues and pull requests to keep track of sub tasks which are too small to be
put into their own issue. This is a nice way to keep closely related things
together, have an indicator of progress, and get a good overview. The progress
is shown in issue lists in the GitHub UI.

## Labels

Labels represent information in different dimensions which are helpful to make
specific information about the issue more visible, to classify issues for easier
listing and filtering, and to assist with the workflow how issues are handled.

The following sections define types of labels in the different dimensions such
as status, type, or component. This includes a description of how each dimension
of labels is supposed to be used and examples for corresponding labels.

### General conventions

Spelling of labels is all lower-case. Words are separated by spaces.

If a label is split in several sub-labels they are indicated by a colon such as
`test: broken`, `test: floating`. This keeps them sorted together in the lists
for selecting labels for assignment or filtering.

Colors are used to group labels.

Common labels should be consistent across repositories but each repository will
also have labels which are only relevant for the specific repository.

### Status

These labels indicate a certain status in the workflow. This adds more
fine-grained status information to the status which already is handled by the
GitHub UI (open, closed, review status of pull requests).

Examples are `wip`, `backport to bitcoin` or `waiting: feedback`.

### Type

This indicates the type of the issue. Each issue MUST have exactly one type.
Issues of the same type should be similar in content, format, and process.

Examples are `bug`, `feature`, `refactoring`.

### Category

These labels indicate a general category. It's usually not tied to a specific
part of the code. It can help with grouping issues together, for example on a
project board, or when filtering work done by specific people or in a specific
way (e.g. security issues).

Issues can have zero, one, or multiple categories.

Examples are `build`, `documentation`, `ci`.

### Component

These labels indicate a specific part of the code. It might also indicate that
special domain knowledge is required to work on these issues.

Issues can have be assigned to zero, one, or multiple components.

These labels are specific per repository.

Examples for the `dtr-org/unit-e` repo are `consensus`, `economics`,
`finalization`.

### Welcome issues

It has become a good practice to indicate issues which are a good starting point
for new people. There are several conventions used for that. We settle on `good
first issue` which is natively supported by GitHub.

### Platform

This is used for flagging platform specific issues.

Examples are `platform: linux`, `platform: windows`.
