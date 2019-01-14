# Conventions for GitHub milestones

[GitHub milestones](https://help.github.com/articles/about-milestones/) are a
good way to group and schedule issues and pull requests, especially towards
releases. Milestones nicely show progress in the form of how many issues and
pull requests assigned to a milestone are already done and how many are still
open.

## Definition of milestones

We use milestones to assign issues and pull requests to releases. Each release
has its own milestone.

## Assigning issues and pull requests to milestones

An issue meant to be fixed in a particular release or a pull request meant to be
merged before a particular release is assigned to the corresponding milestone.

Incoming issues often have no milestone assigned, especially if they are coming
from people not part of the maintainer or developer team. These need to be
triaged and assigned to milestones. This is a way to schedule work and to manage
expectations.

Pull requests don't necessarily have to be assigned to a milestone. They usually
are short-lived and the branch to which they are supposed to be merged already
indicates to which release they are going.

## "Future" milestone

There is a special milestone "Future" which is used to indicate that the issue
won't be handled in any of the upcoming releases. They will be assigned to
release milestones once a release is planned which is supposed to include the
work represented by the issue.

The "Future" milestone should not be used to park work which will never be done.
Those issues should be closed with a friendly explanation why they won't be
addressed in the foreseeable future.

## Alternatives for grouping issues

Sometimes it's advantageous to group issues which belong together in some way or
represent a bigger part of work, which is broken down into more fine-grained
bits. Milestones should not be used for pure grouping of issues. They are meant
to express relation of issues and pull requests to releases.

There are some alternatives for pure grouping of issues:

High-level or meta issues can be created and they can include a [task
list](https://help.github.com/articles/about-task-lists/) in their description
with links to other issues. Progress on these checklists is also shown in the
GitHub UI.

[Project boards](https://help.github.com/articles/about-project-boards/) can be
used to represent bigger streams of work. They allow more fine-grained progress
tracking and prioritization of issues. This is particularly useful for sub
projects which are represented by many issues and which are longer running, also
when spanning more than one release.

For simple grouping in terms of type of work or component
[labels](https://github.com/dtr-org/unit-e-docs/blob/master/project/issues.md#labels)
can be used. Labels should be static, though, and not express time or release
related information.
