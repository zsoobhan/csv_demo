# Demo CSV Parser

[![Build Status](https://travis-ci.org/zsoobhan/csv_demo.svg?branch=master)](https://travis-ci.org/zsoobhan/csv_demo)

## Installation

It is recommended that the installation is performed from within a python 3.6
virtual environment. See virtualenv docs for information on how to set one up.

```shell
    pip install -r requirements.txt
```

## Testing

```shell
    python -m pytest --flake8
```

## Usage

Enter a python shell and do the following:

```python
    >>> import csv_parser
    >>> parser = csv_parser.CSVParser()
    >>> parser.parse()
```

Inspecting parser object:

```python
parser.__str__()  # basic status
parser.directory  # returns directory name
parser._clean_data  # returns validated data parsed
parser._data  # returns data in expected output
```

## Continuous Integration

The tests are run automatically by TravisCI on pushes to master.
Go to the [TravisCI page](https://travis-ci.org/zsoobhan/csv_demo/) to see the 
build output and see `.travis.yml` for the build details.

## Improvements

* `test_csv_parser.py` needs expansion
  - use `mock` to test more input files instead of  `EXPECTED` global variable
  - use pytest fixtures
  - add more than one test

* use pandas module more efficiently (first time using it)
  - read the pandas docs to find out more

* refactor now that we have working test suite.
