# Data Dictionary for Pandas

The `DataDict` class in this package provides functionality for mapping the columns of different pandas data frames into a consistent namespace, ensuring the columns to comply with the data type specified in the data dictionary, describing the data and formatting it.

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

Download the source code by cloning the repository or by pressing ['Download ZIP'](https://github.com/177arc/pandas-datadict/archive/master.zip) on this page.
Install by navigating to the proper directory and running

    python setup.py install

## Usage

### Pure Python with data dictionary data frame

To use a data dictionary data frame to remap columns of a given data frame:
```python
import pandas as pd
from datetime import datetime
from datadict import DataDict

# Create data dictionary from data frame
dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', '{:s}'],
             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
             4: ['data_set_1', 'field_5', 'Name 5', 'Description 5', 'datetime64', '{:%B %d, %Y}']},
       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

# Create example data frame.
data = {0: ['value 1', 1, True, 1.1, datetime(2019, 1, 1)],
        1: ['value 2', 2, False, 1.2, datetime(2019, 1, 2)],
        2: ['value 3', 3, None, None, None]}
data_df = pd.DataFrame.from_dict(data, orient='index', columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5'])

# Remap the columns of the data frame using the data dictionary
df = dd.remap(data_df, 'data_set_1')

# Print the data frame with formatted values
print(dd.format(df))
```

### Pure Python with data dictionary file

To use a data dictionary file, such as [data_dict.csv](https://github.com/177arc/pandas-datadict/blob/master/tests/data_dict.csv), to remap the columns of a data frame:
```python
import pandas as pd
from datetime import datetime
from datadict import DataDict

# Load data dictionary from file
dd = DataDict(data_dict_file='data_dict.csv')

# Create example data frame.
data = {0: ['value 1', 1, True, 1.1, datetime(2019, 1, 1)],
        1: ['value 2', 2, False, 1.2, datetime(2019, 1, 2)],
        2: ['value 3', 3, None, None, None]}
data_df = pd.DataFrame.from_dict(data, orient='index', columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5'])

# Remap the columns of the data frame using the data dictionary
df = dd.remap(data_df, 'data_set_1')

# Print the data frame with formatted values
print(dd.format(df))
```

### Jupyter Notebook
When using the data dictionary within Jupyter notebooks, additional functionality for displaying a data frame is available when importing the `datadict.jupyter` package. For example, to display a data frame with its column descriptions:
```python
import pandas as pd
from datetime import datetime
from datadict.jupyter import DataDict # IMPORTANT: import from datadict.jupyter instead of datadict

# Load data dictionary from file
dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', '{:s}'],
             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
             4: ['data_set_1', 'field_5', 'Name 5', 'Description 5', 'datetime64', '{:%B %d, %Y}']},
       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

# Create example data frame.
data = {0: ['value 1', 1, True, 1.1, datetime(2019, 1, 1)],
        1: ['value 2', 2, False, 1.2, datetime(2019, 1, 2)],
        2: ['value 3', 3, None, None, None]}
data_df = pd.DataFrame.from_dict(data, orient='index', columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5'])

# Remap the columns of the data frame using the data dictionary
df = dd.remap(data_df, 'data_set_1')

# Display the data frame with formatted values and descriptions
dd.display(df)
```
![alt text](https://raw.githubusercontent.com/177arc/pandas-datadict/master/datadict_jupyter_example.png "Data dictionary Jupyter example output")

## Documentation

For the code documentation, please visit the documentation [Github Pages](https://177arc.github.io/pandas-datadict/docs/datadict/).