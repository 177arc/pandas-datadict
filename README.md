[![PyPi Downloads](https://pepy.tech/badge/pandas-datadict)](https://pepy.tech/project/pandas-datadict)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-datadict/month)](https://pepy.tech/project/pandas-datadict/month)
[![PyPi Version](https://badge.fury.io/py/pandas-datadict.svg)](https://pypi.org/project/pandas-datadict/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Data Dictionary for pandas

The data dictionary consists at least of the following columns:
* `Data Set`: Used when mapping in combination with `Field` to rename to the column to `Name`.
* `Field`: Column name of the data frame to map to `Name`.
* `Name`: Column name that is unique throughout the data dictionary.
* `Description`: Description of the column name. This can be used to provide additional information when displaying the data frame.
* `Type`: Type the column should be cast to.
* `Format`: Format to use when values need to be converted to a string representation. The format string has to be a Python format string such as `{:.0f}%`

The data dictionary can either be loaded from a CSV file or from a data frame.

## Installation

### Using pip

You can install using the pip package manager by running

    pip install pandas-datadict

Alternatively, you could install directly from Github:

    pip install https://github.com/177arc/pandas-datadict/archive/master.zip

### From source

Download the source code by cloning the repository or by pressing [Download ZIP](https://github.com/177arc/pandas-datadict/archive/master.zip) on this page.
Install by navigating to the proper directory and running

    python setup.py install

## Usage

For usage guidance and testing the package interactively, hit the [Usage Jupyter Notebook](https://mybinder.org/v2/gh/177arc/pandas-datadict/master?filepath=usage.ipynb).

## Documentation

For the code documentation, please visit the documentation [Github Pages](https://177arc.github.io/pandas-datadict/docs/datadict/).

## Contributing

1. Fork the repository on GitHub.
2. Run the tests with `python -m pytest tests/` to confirm they all pass on your system.
   If the tests fail, then try and find out why this is happening. If you aren't
   able to do this yourself, then don't hesitate to either create an issue on
   GitHub, contact me on Discord or send an email to [py@177arc.net](mailto:py@177arc.net>).
3. Either create your feature and then write tests for it, or do this the other
   way around.
4. Run all tests again with with `python -m pytest tests/` to confirm that everything
   still passes, including your newly added test(s).
5. Create a pull request for the main repository's ``master`` branch.