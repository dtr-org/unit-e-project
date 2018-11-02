*What does it take to make UnitE an awesome open source project? This document outlines a strategy and concrete actions how to get there. It's meant as a starting point which we will refine while going. It's living in the unit-e-docs repo and there are GitHub issues in this repo with further actions and discussions. They are also linked from the corresponding sections of this document.*

The focus of this document is the open source software development of UnitE.

## Goals

* Run UnitE as an open source project according to highest standards
* Make development transparent to the public
* Be open for contributions and create a diverse and distributed community of contributors
* Maintain a welcoming, pragmatic, fun culture focused on getting things done
* Quality over quantity
* Build an engaged user community
* Support DTR foundation in nurturing an ecosystem of projects around UnitE


## Governance

Purpose and direction of the project need to be clear to everyone. This can be captured in some vision or mission document. There is work in progress to put that on the web sites of the foundation and the project which are being created.

Tone and culture of a project are critical to its success in attracting and retaining users and contributors. The most important part is to live the culture by example, be open, be welcoming, be kind. A code of conduct can help to make some part of the culture explicit and have something as guide in case of conflicts.

Decisions have to be taken. Generally, decision making should happen on the most local level. There are still things which need some more central authority to be decided, e.g. what goes into the main branch of the code, what and when is released. That's what maintainers are responsible for. This could be seen as following the principle of subsidiarity.

*It might be worth looking into more broad, more participative decision making in the future, especially for more general decisions and decisions which go beyond just the code.*

### Governance elements

* Project vision (keep it simple)
* Code of Conduct (Examples: [KDE Code of Conduct](https://www.kde.org/code-of-conduct/), [Contributor Covenant](https://www.contributor-covenant.org/))
* Maintainers (define and document who maintainers are and how they are selected, how is access to the git repo managed, who has access, how to get access, put it in a MAINTAINERS.md file)
* License policy
  * MIT for code
    * License file ([COPYING](https://github.com/dtr-org/unit-e/blob/master/COPYING))
    * License headers in each file
  * CC-BY-SA for text and documentation specific to the UnitE project
  * CC-0 for data and text to be used by others
* No contributor agreement, i.e. inbound=outbound (That means only the license governs what can be done with the code, contributors contribute under the same license (inbound) as the project releases the project (outbound). There is nothing like a company releasing a "commercial" version under a proprietary license.)
* Use [DCO](https://developercertificate.org/)?

### Actions

* [Document maintainers](https://github.com/dtr-org/unit-e-docs/issues/17)
* [Create UnitE Code of Conduct](https://github.com/dtr-org/unit-e-docs/issues/18)
* [Decide if to use DCO](https://github.com/dtr-org/unit-e-docs/issues/19)
* [Document license policy](https://github.com/dtr-org/unit-e-docs/issues/20)


## Development

Core and starting point for the open source project is the development of the software. Everything else builds on top of that, users, contributors, scaling the community. It is embedded in the greater context and mission of the foundation and the research which is happening as part and around the project.

### Development process

Ideally there is one documented development process which works the same for everybody, core contributors as well as external contributors.

A good part of the process is already defined by the current practices and by what is inherited from the Bitcoin development process (see Bitcoin Core's [CONTRIBUTING.md](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md)). This might need some adaption where we feel the need to improve on what is there.

#### Git repositories

The central place for development is GitHub and the core code repository ([dtr-org/unit-e](https://github.com/dtr-org/unit-e)). It's currently private but will be made public when we are ready to launch.

The [dtr-org/unit-e-docs](https://github.com/dtr-org/unit-e-docs) repo contains additional documentation which is not directly related to the code of UnitE but is relevant to the project. This includes documentation of architectural decisions, protocol specifications, and processes. The repo will be made public along with the main code repository.

The [dtr-org/clonemachine](https://github.com/dtr-org/clonemachine) repo contains the tooling to prepare a fork of Bitcoin Core which is ready to be merged into the UnitE code base. This repo also will be made public along with the main code repository.

Work on all these repositories like they would already be public in terms of what you put in there.

##### Actions

* [Define repository layout for open source project](https://github.com/dtr-org/unit-e-docs/issues/21)

#### Contributing guidelines

The [CONTRIBUTING.md](https://github.com/dtr-org/unit-e/blob/master/CONTRIBUTING.md) file is the central place to document the development process. There is a [great template](https://github.com/nayafia/contributing-template) for what should be covered there.

The CONTRIBUTING.md file should cover all the following sections of the development process.

##### Actions

* [Refine CONTRIBUTING.md](https://github.com/dtr-org/unit-e-docs/issues/22)

#### Tracking work

Work is tracked in GitHub [issues](https://github.com/dtr-org/unit-e/issues) and [pull requests](https://github.com/dtr-org/unit-e/pulls). Keeping discussions there (or at least referencing them from there) keeps them close to the code and creates transparency.

GitHub [milestones](https://github.com/dtr-org/unit-e/milestones) are used to group and schedule work and [labels](https://github.com/dtr-org/unit-e/labels) to classify issues.

There are templates for issues and pull request which help to make sure that the quality of new ones is high and required information is there. This is especially useful for new and external contributors but can also serve as a reminder and guideline for everybody.

##### Actions

* [Create issue template](https://github.com/dtr-org/unit-e-docs/issues/23)
* [Create PR template](https://github.com/dtr-org/unit-e-docs/issues/24)
* [Define issue labels](https://github.com/dtr-org/unit-e-docs/issues/25)
* [Define milestones](https://github.com/dtr-org/unit-e-docs/issues/26)

#### Architectural decisions

Architectural decisions are taken and documented using the [Architecture Decision Record](https://github.com/dtr-org/unit-e-docs/tree/master/adrs) framework. See [ADR-1](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/2018-08-16-ADR-1%20Adopt%20ADR.md) for more details.

##### Actions

* [Decide on scope and visibility of ADRs](https://github.com/dtr-org/unit-e-docs/issues/27)

#### Coding style

The C++ code follows the [Google C++ style guide](https://google.github.io/styleguide/cppguide.html) with some added specifications where the Google style guide was too generic or justified some decisions based on the actual codebase. It's documented in the [developer notes](https://github.com/dtr-org/unit-e/blob/master/doc/developer-notes.md).

There are automatic checks of the style so that there is a clear baseline and for example code reviews don't have to deal with nitpicking on style. That takes out a whole dimension of issues and discussions.

We have both lint checks (clang-format is part of those) as first stage of the integration pipeline. Furthermore there is a [git hook](https://gist.github.com/Gnappuraz/aa082122ba9ce1c76a4149404f8255ec) to apply style before committing so that is really hard to commit stuff that is not formatted. This uses the [clang-format style file](https://github.com/dtr-org/unit-e/blob/master/src/.clang-format).

The CI runs automatic lint checks. See the lint stage in the [Travis CI configuration](https://github.com/dtr-org/unit-e/blob/master/.travis.yml).

Code and style related issues are tracked under the [code style and naming](https://github.com/dtr-org/unit-e/labels/code%20style%20and%20naming) label.

##### Actions

* [Merge style guide bits from unit-e-docs repo into standard place in developer notes](https://github.com/dtr-org/unit-e-docs/issues/28)
* [Document how to apply code style checks](https://github.com/dtr-org/unit-e-docs/issues/29)

#### Upstream integration

[UnitE](https://github.com/dtr-org/unit-e) is a code fork of [Bitcoin Core](https://github.com/bitcoin/bitcoin). The Bitcoin Core code is copied and adapted to the UnitE namings through [clonemachine](https://github.com/dtr-org/clonemachine). Then it is merged with the UnitE specific changes. This is eventually repeated when a new version of Bitcoin Core is released. Not all releases are merged.

Possible improvements to the cloning process:

* [Refinements of cloning](https://github.com/dtr-org/unit-e/issues?q=is%3Aissue+is%3Aopen+label%3A%22upstream+sync%22)
* [Format code according to style guide](https://github.com/dtr-org/unit-e/issues/60)
* Make sure docs reflect UnitE and not refer to Bitcoin Core, especially when it's about URLs or other pointers
* CI which does regular runs of clonemachine so that changes in Bitcoin Core which break clonemachine or will cause exceptional work for the merge are detected early
* Document best practices to avoid creating merge problems (such as using adaptors or structuring files so that they don't create conflicts)

#### Commit guidelines

Guidelines covering:

* Content of commits
* Style of commit messages
* What meta info to put into commits such as git trailers, references, GitHub commands
* If and how to sign commits
* Structuring pull request
* What history to keep and what to squash

##### Actions

* [Document commit guidelines](https://github.com/dtr-org/unit-e-docs/issues/30)

#### Review process

How to review pull requests, conventions for asking for review and how to give feedback and approval or disapproval. This mostly follows the upstream conventions.

All changes have to go through review by at least one other developer.

All changes need to have successful CI runs before they can be merged. This is integrated in the pull request process via the GitHub APIs.

##### Actions

* [Define review process](https://github.com/dtr-org/unit-e-docs/issues/31)
* [Run tests on pull requests](https://github.com/dtr-org/unit-e-docs/issues/32)

#### Git branches

On which branches to work, release, stable, integration, development branches.

##### Actions

* [Define branching model](https://github.com/dtr-org/unit-e-docs/issues/33)

#### Bug reports and feature requests

Bugs should be reported as GitHub issues or fixed directly in pull requests if trivial enough.

Feature request should be reported as GitHub issues as well and go through a similar process.

With raising volume of issues we need to define an approach to triaging bugs.

### Developer tooling

Tooling for developers to work on the code. *Needs more details.*

* Build environment
* Local test setup
* [CI](https://travis-ci.com/dtr-org/unit-e) (a subset should run on pull requests as well to give early feedback, badges about state of CI should be shown in README)
* Bots, doing mundane tasks such as checking style and formatting, keeping track of issues, etc. Bots need a bit of an identity so that it's clear what they do, who has control, etc. There are teams who [treat bots as team members](https://media.ccc.de/v/ASG2017-130-cyborg_teams).
* Test network for tests in a production-like scenario

#### Actions

* [Document developer tooling](https://github.com/dtr-org/unit-e-docs/issues/34)

### Releases

It's all about shipping, so the release process is central and crucial. The UnitE release process will inherit parts from the [Bitcoin release process](https://github.com/bitcoin/bitcoin/blob/master/doc/release-process.md) but be improved and adapted to our needs.

Things to be taken care of:

* Changelog, release notes (Bitcoin does it nicely. e.g. their [0.17.0 release notes](https://bitcoin.org/en/release/v0.17.0))
* Versioning, need to agree on a scheme, [Semantic Versioning](https://semver.org/) is a popular one (gather input for versioning scheme, major (breaking changes), minor (compatible changes), patch (bug fixes), what about hard fork, soft fork, p2p protocol version, blockchain version)
* Building release artifacts, binaries to be distributed to users on the various platforms in as native form as possible. This might for example involve packaging for Linux distributions.
* Where to publish releases? GitHub releases? Own servers?
* Reproducible builds (Bitcoin uses [Gitian](https://gitian.org/)) to allow users to validate binary builds without having to trust a single entity
* Release signing to give users a secure way to check where the release is coming from. Which keys to use? Where to run the signing?
* On which platforms to release? Bitcoin does arm, arm64, osx, osx64, win32, win64, linux-i686, linux-x86_64. Do we need 32 bit platforms? Can we start with a smaller set to keep build and test matrices small?
* Public roadmap and release planning to make it transparent what is happening and what users can expect
* Define support for older releases (such as providing bug fixes or security fixes)

#### Actions

* [Set up release pipeline](https://github.com/dtr-org/unit-e-docs/issues/35)
* [Define versioning scheme](https://github.com/dtr-org/unit-e-docs/issues/36)
* [Roadmap for releases](https://github.com/dtr-org/unit-e-docs/issues/37)
* [Define support policy](https://github.com/dtr-org/unit-e-docs/issues/38)

### Security

Security issues need to be handled with special care.

* Way to report security issues privately (security@unit-e.org?)
* CVE process?
* Security bug bounties (e.g. work with [HackerOne](https://www.hackerone.com/))

#### Actions

* [Set up email address for reporting security issues](https://github.com/dtr-org/unit-e-docs/issues/39)


## User community

We have released something. Now we will get users. This is why we are doing it. We want to make users happy, make sure they have a good experience with our software. We also want to have their feedback and input.

We also want users to become contributors. That's what is covered in the next section. Building the contributor funnel, turning users into contributors into maintainers.

### User support and communication

Users will need a way to get support. The core team can help here at the beginning but the only way to scale that is to engage the community.

There is a study about [how the top 100 projects on GitHub do user support](https://github.com/nayafia/user-support). Running an own forum for user support seems to be the most popular option beyond GitHub issues. Other options are mailing lists, IRC, Gitter, Slack, or StackExchange.

Forums tend to work well for users, the other options work better for developers.


## Contributor community

Contributions can come in many ways. People might contribute code as patches for bug fixes or new features. They also might contribute other things such as documentation, translations, web or graphical design. Or they engage in activities such as user support, bug triaging, promotion. Or they create and run projects which are related to UnitE but are not part of the core, such as additional web sites or services, or alternative clients, wallets, etc.

We do want to support all of that in a scalable and sustainable way.

We do want to provide users a path to become contributors and gradually take responsibility.

### Responsiveness

One of the key factors in retaining new contributors is responsiveness. A [study by Mozilla](https://docs.google.com/presentation/d/1hsJLv1ieSqtXBzd5YZusY-mB8e1VJzaeOmh8Q4VeMio/edit#slide=id.g43d857af8_0177) showed that contributors who got a response in less than 48 hours have an exceptionally high chance of continuing to contribute while contributors who waited more than 7 days almost never came back.

We need to track response times and work out mechanisms how to keep them low.

#### Actions

* [Track response time on issues](https://github.com/dtr-org/unit-e-docs/issues/40)

### Mentoring

One of the most effective ways to get new contributors and to help to create a diverse community is mentoring. This can for example be done in the form of structuring and helping entry level tasks to be picked by new people or as more formal programs such as [Google's Summer of Code](https://summerofcode.withgoogle.com/) or [Outreachy](https://www.outreachy.org/).

### Metrics

There is the German saying "Wer viel misst, misst viel Mist" ("If you measure a lot you will measure a lot of crap" or something like that) but there is some use for metrics to get insight into the community, become aware of trends, and have a way to evaluate changes and experiments on the community level.

Useful metrics to watch:

* Downloads (to measure popularity)
* Number of contributors (to measure community size)
* Number of contributors by affiliation (to measure community diversity)
* Contributor retention (to have an indication for the openness and attractiveness of the project)
* Contributors per area of the project (to identify areas which don't get enough attention)
* ...

There are a couple of tools around to do open source metrics, e.g.:

* [Bitergia](https://bitergia.com/)
* [Stackalytics](http://stackalytics.com/)

### Outreach

The word needs to be spread to engage people. Things to do there:

* Creating and publishing content:
  * Announcements
  * Blogs
  * Weekly reports about project activity
* Organizing events
  * Meetups
  * Hackathons
  * Conferences
* Ambassador program to enable and recognize community members talking about the project
* Office hours of the development team
* Holding AMAs on Reddit
* Merchandize
  * Stickers
  * T-Shirts
  * ...
* Press coverage
* Interviews with core developers (such as [The people behind the code](https://github.com/open-source/stories))
* ...

### Outbound community engagement

To be a good citizen in the overall open source community and to benefit from the collaboration and input from the many smart people which are around there it's important to engage with other open source projects and the community in general. This is also very important for us to build a good reputation, which in the end is the currency of open source.

One effective way is to give back, to contribute to other projects, especially those we rely on. This can happen in various forms:

* Contributing code or feedback to Bitcoin or other projects we directly rely on
* Attending events of other community projects
* Sponsoring events

The other effective way is spreading the word:

* Talk at open source conferences such as [FOSDEM](https://fosdem.org/2019/), [Open Source Summit](https://en.wikipedia.org/wiki/Open_Source_Summit), [OSCON](https://en.wikipedia.org/wiki/O%27Reilly_Open_Source_Convention) or on the many smaller events.
* Talk at crypto conferences
* Talk at meetups (where conveniently possible)


## Scaling community

If we do things right we will have a growing community. How do we scale that? We do want valuable projects to be created around UnitE and we do want to increase the number of people involved beyond what we can directly handle in the core team.

We need to establish a way of cooperation which allows people to do their own work without the need to coordinate closely as it is needed when collaborating on the core software. This extends beyond the purely technical work.

Bicoin is a superb example for projects which grew around it.

Things to look into:

* Additional services (developed in cooperation or by the wider community or bootstrapped by the core team to allow others to build on it)
  * Block tracker
  * Node explorer
  * Alternative clients
  * Network statistics (see [Statoshi](https://statoshi.info/))
  * Performance benchmarks (see https://bitcoinperf.com/about/)
  * Tracking pull requesrts (see https://bitcoinacks.com/)
* Support local groups, meetups
* ...

## Communication channels

Communication is essential and to support a growing, distributed community it needs appropriate communication channels.

Roughly we need three different types of channels:

* One way communication to the outside for announcements, documentation, etc.
* Asynchronous bi-directional communication for questions, contributions which are not done in real-time
* Synchronous bi-directional communication for direct interaction
* A dedicated asynchronous channel for security critical bug reports

One important decision is if we want to host infrastructure ourselves or we rely on third party services. A related question is if to rely on services based on proprietary software or if to insist on services based on free software which could be run by ourselves or others as well.

### Tools

* Home page and other web pages
* GitHub (issues, pull requests)
* Mailing lists (e.g. [Mailman](http://www.list.org/))
* Forums
  * [Discourse](https://www.discourse.org/)
* Chat
  * [Slack](https://slack.com)
  * [Mattermost](https://mattermost.com/) (open source Slack clone)
  * [RocketChat](https://rocket.chat/) (open source Slack clone)
  * [Telegram](https://telegram.org/)
  * IRC (valued by the traditionalists)
  * [Gitter](https://gitter.im/) (simple chat, which can easily be added to any repo, owned by GitLab, not too powerful)
  * Video Chat
    * [Hangouts](https://hangouts.google.com/)
    * [Appear.in](https://appear.in/)
    * [Zoom](https://zoom.us/) (maybe the best video conferencing option right now, scales to large number of participants)

### Actions

* [Decide on community communication channels](https://github.com/dtr-org/unit-e-docs/issues/41)


## Documentation

Documentation spans all areas of the project. There are two main target groups, users and contributors. There might be a third group with 3rd party developers using our technology but not contributing to the project itself. And there is a fourth area of documenting the project itself, that's kind of meta documentation, governance documents, etc.

According to [GitHub's Open Source Survey in 2017](http://opensourcesurvey.org/2017/) documentation is highly valued but perceived as the number one issue in open source projects. Projects with great and up to date documentation set themselves apart as excellent examples.

Creating documentation is essential but it's also essential to establish a low-barrier way for many people to contribute to documentation. Especially with many people contributing, keeping documentation structured takes effort, but it's worth it, because it keeps quality high (addressing the number one issue) and reduces the overall effort to maintain it (because there is less of a mess).

See [documentation.md](documentation.md) for details about our approach to documentation.


## Translations

Many end users expect software to be available in their native language. This can be achieved by translating software and documentation targeted at end users. It requires internationalization (i18n), i.e. enabling the software to be translated, as well as localization (l10n), i.e. actually providing translated texts and other adaptions to local norms such as date or number formats.

Documentation and tools targeted as developers are not translated, but English is used as the standard language. While this might provide some barrier for developers who are not fluent in English, it helps a lot with communication as one community.

See [documentation.md](documentation.md) for details about our approach to translating documentation.

### Actions

* [Translations](https://github.com/dtr-org/unit-e-docs/issues/44)


## Funding

The project is funded right now. It might need some thinking about how to sustain that long-term. Some general thoughts about open source project funding are in [Nadya Eghbal's "Lemonade Stand"](https://github.com/nayafia/lemonade-stand).


## References

References to some general guides and documents about running open source projects:

* https://opensource.guide/
* http://www.artofcommunityonline.org/
