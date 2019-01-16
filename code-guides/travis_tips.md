# Travis tips

Contains different tips for travis CI.

## travis.yml

Unlike other CI systems Travis stores almost all
run/build configurations in your repository.
The most important file for this is `.travis.yml`, located in the root
of the project.
In case of unit-e there are also some other files in `.travis` folder.

## Setup personal travis builds

The 'central' travis build is [here](https://travis-ci.com/dtr-org/unit-e)
and it is triggered on each PR. If you need to run travis builds without
having a PR, you can configure you own travis build for that:

Go to [travis settings](https://travis-ci.com/account/repositories) and
activate the integration with the repository you would like to run tests on.

In unit-e we also configure travis to only run on master branch(`.travis.yml`):
```
branches:
  only:
    - master
```

You might need to change that for your branch.

Limitations:
- In the free version you can only run 100 builds
- Free builds are also very slow
- Since everything is slower - jobs might reach the 50 minute timeout =>
test results won't be displayed

Short summary of steps:
1) Activate travis integration [here](https://travis-ci.com/account/repositories)
2) Add repositories you would like to run tests on
3) Create and checkout the git branch
4) Replace `master` at the beginning of `.travis.yml` with your branch name
5) Commit 4 and push to your repository
6) Check for your build in [travis dashboard](https://travis-ci.com)

## Repeat tests many times (Unit-e)

This is useful if you are suffering from flaky tests.
You can reproduce flakiness or kind of proof that the test is not flaky anymore.

Start with configuring personal travis builds.
Then go to `test_runner.py`, locate the `run_tests` function and redefine `test_list`
to be `test_list = ['test you want to repeat] * 50`. Commit this change.

- **Do not forget to revert all changes made to the scripts/travis configs before you merge**
- You can cancel jobs that do not run functional tests to save some time
- Do not repeat tests too many times. You can easily hit 50 minute job
limit and not receive results at all
- You _can_ do this in PR builds, but the changes you make will be visible
in the PR. Also you would need to be extra careful not to merge them.