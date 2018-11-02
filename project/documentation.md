# UnitE Documentation

Documentation is an essential part of an open source project. It's one of the
critical factors for adoption by users and for creating an open contributor
community.

This document defines what documentation we need, for which audience it is, and
how we maintain it.

The general documentation of the project on the high level, including foundation
and general vision is out of the scope of this document. It will be covered on
the project and foundation web sites.

The list describes a desirable state. The effort to get there and what to do in
which order needs to be prioritized.

Generally we do want to make it easy for everybody to contribute to the
documentation while maintaining a high level of quality. We strive for making
the documentation a collaborative effort between developers, writers, and users.

## Audience

We have documentation targeted at two main personas, users and developers. There
also is a spectrum in between, for example where users look into technical
details of the project to assess its viability or to understand how it works.

We do want to encourage users to evolve into contributors. Documentation and
contributing to documentation provides a great path for that.

## Structure

We will create a documentation site which spans the audience from users to
developers. The different chapters will indicate requirements and specific
audience. It will start with general and user focused documentation and go with
increasing technical depths to developer documentation intended for people who
want to contribute to the code.

The content of the site will be hosted in git and managed with the usual
decentralized contribution process.

### Outline

* Introduction
  * What is UnitE?
  * Reference to project web sites
  * What is this documentation about and where to find more
* Using UnitE
  * Using a wallet
  * Keeping keys safe
  * Making transactions
  * Where to find more information
  * How to get support
* Running a node
  * Running a full node
  * Running a proposer
  * Running a validator
  * Security considerations
  * Availability considerations
* Conceptual technical documentation
  * Resources (research, architecture & design documents, ADRs)
  * Protocol documentation - Documentation of the network protocol
  * Testnet
* Developer documentation
  * Import and adapt content from bitcoin.org
  * Aggregate docs from unit-e repo
  * Resources for contributors

### Sources

The documentation is coming from various places. We do want to provide users a
consistent view and entry point for all documentation. This is a list of
documentation sources we use. How they are integrated in detail is to be
determined.

* Original documentation hosted in unit-e-docs
* Built-in documentation of the various tools, such as command line help, man
  pages, built-in help, or application manuals.
* README.md - central entry point for open source project
* CONTRIBUTING.md - information how to contribute, includes documentation of
  development process
* Code documentation - Doxygen generated documentation of code, including APIs
* Developer documentation - various documents in the `docs` directory with
  details about everything relevant for people working on or directly with the
  code
* Architecture and design documents (ADRs) - Discussing and documenting
  architectural decisions of the project
* External material such as from bitcoin.org.

## Translations

English is the primary language for the documentation. Especially the
documentation targeted at users should also be available in translations to
other languages to address a wider audience.

The tooling needs to be chosen to allow for future translations. Exact
definition of to which languages to translate and how the process will look like
will be defined later.

## References

### Documentation tools

* [ReadTheDocs](https://readthedocs.org/) - Rendering and hosting documentation
  written in [Markdown](https://daringfireball.net/projects/markdown/syntax),
  published on push into git repo
* [Asciidoctor](https://asciidoctor.org/) - Tool to render AsciiDoc, which is
  similar to Markdown but more powerful (with power also comes some more
  complexity)
* [Jekyll](https://jekyllrb.com/) - Popular static site generator, written for
  blogs, but can also be used for generic web sites and documentation
* [Hugo](https://gohugo.io/) - Static site generator, suitable for
  documentation, faster than Jekyll for big sites
* [GitHub Wiki](https://help.github.com/articles/about-github-wikis/) - GitHub's
  builtin Wiki backed by git, allows more informal contribution, harder to
  structure and review
* [Sphinx](http://www.sphinx-doc.org/en/master/index.html) - Documentation
  generator originating from the Python community, used by quite some projects.
  Integrates with readthedocs.org. Uses
  [reStructuredText](http://docutils.sourceforge.net/rst.html) as markup
  language.

### Translation tools

* [Weblate](https://weblate.org)
* [Transifex](https://www.transifex.com/)

### Examples

Some examples of good documentation from other open source projects.

* [bitcoin.org](https://bitcoin.org/en/)
* [Bitcoin Wiki](https://en.bitcoin.it/wiki/Main_Page) (MediaWiki, maybe not a
  great example for documentation but quite some of the content could be
  relevant to us as well)
* [Cosmos](https://cosmos.network/docs/) ([created from
  Markdown](https://github.com/cosmos/cosmos-sdk/blob/develop/docs/DOCS_README.md))
* [Docker](https://docs.docker.com/) ([created from Markdown with
  Jekyll](https://github.com/docker/docker.github.io))
* [Django](https://docs.djangoproject.com) ([created from reStructuredText with
  Sphinx](https://docs.djangoproject.com/en/2.1/internals/contributing/writing-documentation/))
* [Ethereum Homestead](http://www.ethdocs.org) ([created from Markdown with
  ReadTheDocs](http://www.ethdocs.org/en/latest/about.html))
* [Saltstack](https://docs.saltstack.com/en/latest/) (very polished
  documentation, creates with Sphinx and a custom theme)
