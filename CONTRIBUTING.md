# Contributing

Awesome that you are considering to contribute! This guide explains how the
development process works, and how you can easily contribute to the package.

## Install

Install the package in development mode in your environment using:

## Conda

For a conda environment do:

``` bash
conda activate <env-name>
pip install -e .[test]
```

## Venv

For a pip environment do:

``` bash
python -m venv venv/
source ./venv/bin/activate
pip install -e .[test]
```

# Testing

To verify that the application works as expected, we apply testing. We use two
types of testing: static and unit.

## Static analysis

For performing static analysis we use
[Pre-Commit](https://calmcode.io/pre-commit/the-problem.html). Pre-commit allows
us to easily run a suite of tests, as defined in the
[.pre-commit-config.yaml](.pre-commit-config.yaml) in the project. Pre-commit checks
consists of but is not limited to:

* Trivial checks:
	* The encoding of the files
	* If it is valid Python in the files
	* If the YAML files are nicely formatted
	* The code is free of debug statements
* [**Flake8**](https://pypi.org/project/flake8/) is a Python library that wraps
  PyFlakes, pycodestyle and Ned Batchelder's McCabe script. It is a great
  toolkit for checking your code base against coding style
  ([PEP 8](https://www.python.org/dev/peps/pep-0008/), programming errors (like
  “library imported but unused” and “Undefined name”) and to check complexity.
* [**Black**](https://github.com/psf/black) is the Python code formatter and
  makes sure that we format our Python code in the same way. By using it, you
  agree to cede control over minutiae of hand-formatting. In return, Black gives
  you speed, determinism, and freedom from pycodestyle nagging about formatting.
  You will save time and mental energy for more important matters.
* [**MyPy**](https://github.com/python/mypy) is an optional static type checker
  for Python. You can add type hints
  ([PEP 484](https://www.python.org/dev/peps/pep-0484/)) to your Python
  programs, and use mypy to type check them statically. Find bugs in your
  programs without even running them!

If you want to run this automatically before each commit, you can install it as
a pre-commit hook:

``` bash
pip install pre-commit  # install the package in your environment
pre-commit install      # add the git hook
```

You can run `pre-commit` manually using:

```bash
pre-commit run --all-files
```

## Unit testing

For running unit and integration tests we use `pytest`. You can run the tests
using:

```bash
pytest tests/
```

Unit tests are the lowest level of tests, and should test isolated pieces of
code. For example, testing an Apache Spark UDF is a perfect example:

```python
from pyspark.sql.functions import udf

@udf("int")
def add(a: int, b: int) -> int:
    return a + b
```

And in the test file:
```python
import add

def test_add_udf():
  assert add(19, 25) == 44
```

For example, if someone writes a complex regular expression, then you
want to make sure that it is properly covered by unit-tests. The `spark_session`
is automatically generated in the background thanks to the
[`pytest-spark`](https://pypi.org/project/pytest-spark/) package.
