# Prerequisites

* Push and merge rights for this repo.
  [pytest-dbt-core repo](https://github.com/godatadriven/pytest-dbt-core),
  also referred to as the *upstream*.
* A UNIX system that has:
  - `git` able to push to upstream

# Release

Run the release command and make sure you pass in the desired release number:

``` bash
$ python -m pip install gitpython
$ python scripts/release.py --version <my version number>
```

Create a pull request and wait until it the CI passes. Now make sure you merge
the PR and delete the release branch. The CI will automatically pick the tag up
and release it, wait to appear in PyPI. Only merge if the later happens.
