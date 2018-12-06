# Checklist for creating new repositories

When creating new repositories which are meant to be open source we need to set
them up with a little bit of configuration and documentation so that they work
nicely as open source project, adhere to our conventions, and fit into the
overall set of repositories. Here is a checklist of what to do. You can copy
that into an issue if you want to keep track of the different tasks and check
them off there.

* [ ] Create README
* [ ] Document how to run and test the project
* Check that license is stated clearly
  * [ ] License note in README
  * [ ] License file in root directory
  * [ ] Add license headers to all source files. Can be done with
    [`copyright_header.py`](https://github.com/dtr-org/unit-e/blob/master/contrib/devtools/copyright_header.py)).
    Run `copyright_header.py insert <filename>` to add headers and
    `copyright_header.py report <directory>` to check the repository for headers
* [ ] Copy [code of conduct](https://github.com/dtr-org/unit-e/blob/master/CODE_OF_CONDUCT.md) from unit-e repo
* [ ] Create a CONTRIBUTING.md. This should refer to the [unit-e CONTRIBUTING.md](https://github.com/dtr-org/unit-e/blob/master/CONTRIBUTING.md)
  because that contains detailed instructions about the general process but
  point out any special considerations for the new repo.
* Templates
  * [ ] Take
    [.github/ISSUE_TEMPLATES](https://github.com/dtr-org/unit-e/tree/master/.github/ISSUE_TEMPLATE)
    from unit-e and adapt
  * [ ] Take
    [.github/PULL_REQUEST_TEMPLATE.md](https://github.com/dtr-org/unit-e/blob/master/.github/PULL_REQUEST_TEMPLATE.md)
    from unit-e and adapt
* Repository settings (needs admin access)
  * [ ] Disable merging and rebasing pull request on merge
  * [ ]  Set up `master` as protected branch which requires review on pull
    requests and requires status checks to pass, including administrators
  * [ ] Enable [Mergeable app](https://github.com/apps/mergeable) (add
    [configuration](https://github.com/dtr-org/unit-e/blob/master/.github/mergeable.yml))
  * [ ] Enable [DCO app](https://github.com/apps/dco)
