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