# Data Dictionary for Pandas

The `DataDict` class in this package provides functionality for mapping the columns of different pandas data frames into a consistent namespace,
ensuring the columns to comply with the data type specified in the data dictionary and describing the data.

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

[![PyPi Downloads](https://pepy.tech/badge/pandas-datadict)](https://pepy.tech/project/pandas-datadict)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-datadict/month)](https://pepy.tech/project/pandas-datadict/month)
[![PyPi Version](https://badge.fury.io/py/pandas-datadict.svg)](https://pypi.org/project/pandas-datadict/)

You can install using the pip package manager by running

    pip install pandas-datadict

Alternatively, you could install directly from Github:

    pip install https://github.com/177arc/pandas-datadict/archive/master.zip

### From source

Download the source code by cloning the repository or by pressing [Download ZIP](https://github.com/177arc/pandas-datadict/archive/master.zip) on this page.
Install by navigating to the proper directory and running

    python setup.py install

## Usage

### Just Python

To use a data dictionary file, such as ([data_dict.csv](https://github.com/177arc/pandas-datadict/blob/master/tests/data_dict.csv), to remap the columns of a data frame:
```python
import pandas as pd
from datadict import DataDict

dd = DataDict(data_dict_file='data_dict.csv')

data = {0: ['test 1', 1, True, 1.1, datetime(2019, 1, 1)],
        1: ['test 2', 2, False, 1.2, datetime(2019, 1, 2)],
        2: ['test 3', 3, np.nan, None, None]}
data_df = pd.DataFrame.from_dict(data, orient='index', columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5'])
print(dd.remap(data_df, 'data_set_1'))
```

### Jupyter Notebook
