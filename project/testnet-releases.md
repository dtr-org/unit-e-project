# Testnet releases

In order to have a well-defined way to do changes which affect the testnet and
manage breaking changes we define some conventions on testnet releases,
corresponding branches and where and how to apply changes. This gives us a way
to have rapid ongoing development on new features and fixes while still having a
procedure to keep the testnet in a defined state.

## Development branch

Development is happening on the `master` branch in the
[unit-e](https://github.com/dtr-org/unit-e) repository. This branch always
reflects the latest state.

The `master` branch is stable in the sense that it is functional and all tests
pass, but it will introduce changes from time to time which change the protocol
or internal state in an incompatible way. These changes are reviewed and
coordinated through the normal pull request process. You will need to follow
these to keep up to date and to know what to do to run a node from the master
branch. This is something mostly for developers who work on the code.

## Testnet branch

There is a permanent branch `testnet` which reflects the version of the unit-e
client which is compatible with the testnet.

The testnet branch is updated from master when doing testnet deployments. If
this involves breaking changes which require updates or other actions to be able
to connect to the testnet these are announced on the [announcement
page](https://docs.unit-e.io/announcements.html).

To make sure everyone is running a compatible version, the genesis block is
changed when breaking changes are deployed. That gives a more immediate error
message to users because incompatible clients won't sync from the start and not
error out later or being banned.

If there are fixes required for the testnet which can't be done by a full update
from the master branch, they are done through cherry-picks or backports of
commits from master to the testnet branch.

## Testnet releases

A testnet release is an ultra light-weight release of the client code which only
consists of merging the code to the testnet branch. This is independent of
actual client releases which come with version number updates and changelogs.
The git commit log is the reference for what changes are active on the testnet.

The testnet release follows these steps:

1. Merge code from the `master` branch to the `testnet` branch.
1. If there are changes which need to be announced, add an entry to the
   [announcements
   page](https://github.com/dtr-org/docs.unit-e.io/blob/master/announcements.rst).
1. Deploy testnet nodes from the `testnet` branch
