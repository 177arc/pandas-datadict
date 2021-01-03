import pandas as pd
import numpy as np
import warnings
import os
import functools
import pickle
from os import path
from pandas.api.types import is_numeric_dtype
from typing import Dict


class DataDict:
    """
    This class provides functionality for mapping the columns of different data frames into a consistent namespace,
    ensuring the columns to comply with the data type specified in the data dictionary and describing the data.

    The data dictionary consists at least of the following columns:
    * `Data Set`: Used when mapping in combination with `Field` to rename to the column to `Name`.
    * `Field`: Column name of the data frame to map to `Name`.
    * `Name`: Column name that is unique throughout the data dictionary.
    * `Description`: Description of the column name. This can be used to provide additional information when displaying the data frame.
    * `Type`: Type the column should be cast to.
    * `Format`: Format to use when values need to be converted to a string representation. The format string has to be a Python format string such as `{:.0f}%`

    The data dictionary can either be loaded from a CSV file or from a data frame.
    """

    _data_dict_file: str
    _data_dict_updated: float = None
    _data_dict: pd.DataFrame
    _formats: dict
    _names: list

    auto_reload: bool
    column_names = ['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']
    supported_types = ['float', 'float32', 'float64', 'int', 'int32', 'int64', 'object', 'str', 'bool', 'datetime64', 'timedelta', 'category']
    stats = {'sum': 'Total', 'mean': 'Average'}
    meta: object

    def auto_reload(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.auto_reload:
                self.__load()

            return func(self, *args, **kwargs)

        return wrapper

    def __aggr(self, series: pd.Series):
        funcs = self._data_dict[self._data_dict['Name'] == series.name]['Default Aggregation'].values
        try:
            return eval('series.' + funcs[0]) if len(funcs) == 1 and not funcs[0].isspace() else None
        except:
            return None

    @property
    def data_dict(self) -> pd.DataFrame:
        """
        Data dictionary as a data frame.
        """
        return self._data_dict

    @property
    def formats(self) -> Dict[str, str]:
        """
        Dictionary that maps the columns to names to their format strings.
        """
        return self._formats

    def __init__(self, data_dict_file: str = None, auto_reload: bool = True, data_dict: pd.DataFrame = None):
        """
        Creates the data dictionary and validates it. It can either be initialised from a CSV file or a data frame.

        Args:
            data_dict_file: The data dictionary file in CSV format to use to initialise the data dictionary.
            auto_reload: Whether the data dictionary should automatically check for changes in the data dictionary file.
            data_dict: The data dictionary as a data frame to use to initialise the data dictionary instead of the data dictionary file.
        """
        if data_dict_file is not None and data_dict is not None:
            raise ValueError('Parameters data_dict_file and data_dict can\'t be assigned at the same time.')

        self._data_dict_file = data_dict_file
        self.auto_reload = auto_reload
        self.__set_data_dict(data_dict)

        self.__load()

    def __load(self) -> None:
        """
        Loads the data dictionary from the CSV file specified during initialisation and validates it.
        """
        if self._data_dict_file is None:
            return

        if not path.exists(self._data_dict_file):
            raise ValueError(f'The data dictionary file {self._data_dict_file} does not exist.')

        if self._data_dict_updated is not None and os.path.getmtime(self._data_dict_file) == self._data_dict_updated:
            return

        data_dict = pd.read_csv(self._data_dict_file)
        self._data_dict_updated = os.path.getmtime(self._data_dict_file)

        self.__set_data_dict(data_dict)

    def __set_data_dict(self, data_dict: pd.DataFrame) -> None:
        """
        Sets a new data dictionary frame validates it.

        Args:
            data_dict: Specifies the data dictionary.
        """
        DataDict.validate(data_dict)

        self._data_dict = data_dict

        if data_dict is not None:
            formats = self._data_dict[['Name', 'Format']].dropna(subset=['Format'])
            self._formats = pd.Series(formats['Format'].values, index=formats['Name']).to_dict()
            self._names = list(self._data_dict['Name'].values)

    @staticmethod
    def validate(data_dict: pd.DataFrame) -> None:
        """
        Validates the given data dictionary and raises a `ValueError` if the validation fails.

        Args:
            data_dict: The data dictionary to validate.

        Returns:

        Raises:
            ValueError: If the given data dictionary is not valid.
        """
        if data_dict is None:
            return

        data_dict = data_dict.copy()

        # Check that all expected columns exist.
        if not set(data_dict.columns) >= set(DataDict.column_names):
            raise ValueError(f'The data dictionary must at least include the following column names: {DataDict.column_names}')

        # Check that all types are supported Python types.
        if not set(data_dict['Type'].values) <= set(DataDict.supported_types):
            raise ValueError(
                f'The Type column of the data dictionary contains the following unsupported types {set(data_dict["Type"].values) - set(DataDict.supported_types)}. Only the following types are supported: {DataDict.supported_types}')

        # Check that names are unique.
        if any(data_dict['Name'].duplicated()):
            raise ValueError(f'The Name column contains the following duplicates: {data_dict["Name"][data_dict["Name"].duplicated()].values}. The names must be unique.')

        # Check that dataset and field combination is unique.
        data_dict = data_dict.replace('', np.nan)
        data_dict['Field ID'] = data_dict['Data Set'] + '.' + data_dict['Field']
        if any(data_dict['Field ID'][data_dict['Field ID'].isnull() == False].duplicated()):
            raise ValueError(f'The combination of columns Data Set and Field contains the following duplicates: {data_dict["Field ID"][data_dict["Field ID"].duplicated()].values}. The combination must be unique.')

    @staticmethod
    def __str_to_bool(value: str) -> object:
        """
        Converts the given string to a bool if the argument is a string otherwise it returns the value untouched. `yes`, `true`, `1` are considered `True`, the rest is considered `False`.

        Args:
            value: The value to convert to a bool.

        Returns:
            The converted bool if the value is a string. Otherwise the value passed in the argument.
        """
        if pd.isnull(value):
            return None

        if not isinstance(value, str):
            return value

        return value.lower() in ['yes', 'true', '1']

    def df(self, data_set: str = None, any_data_set: bool = False) -> pd.DataFrame:
        """
        Gets the data set with the given name as a data frame.

        Args:
            data_set: The data set to filter by. If this value matches a value in the `Data Set` column of the data dictionary, the matching rows are returned.
            If `data_set` is not specified, the entries with empty `Data Set` are returned.
            any_data_set: Whether to return all data sets in the data frame.

        Returns:
            The data set as a data frame, index by the `Field` column.
        """
        if any_data_set and data_set is not None:
            raise ValueError('Either data_set can be provided or any_data_set can be True but not both.')

        if data_set is None:
            data_set = ''

        return self._data_dict[(self._data_dict['Data Set'] == data_set) | any_data_set].set_index('Field')

    @auto_reload
    def remap(self, df: pd.DataFrame, data_set: str = None, ensure_cols: bool = False, strip_cols: bool = False) -> pd.DataFrame:
        """
        Renames the columns in the given data frame based on based on the `Data Set` and `Field` attributes in the data dictionary to `Name`
        if such a mapping found and converts the columns data to `Type`. It also reorders the columns based on the order of the data dictionary entries.

        Args:
            df: The data frame to remap.
            data_set: The data set to use. If this value matches a value in the `Data Set` column of the data dictionary, then the corresponding names in the `Field`
                column are used to rename the columns of the given data frame to the `Name` column name. If `dataset` is not specified, the values in `Field` column
                that have entries with empty `Data Set` are used.
            ensure_cols: Ensures all columns in the data_set are present. If the source data frame does not contain them, empty ones are created. This parameter can
                only be true if data_set is specified. This is useful when the data frame to be remapped may not have all the columns if it is empty.
            strip_cols: Whether to remove all columns that are not in the data set. In any case, it will leave the index untouched.

        Returns:
            The remapped data frame.
        """
        if df is None:
            raise ValueError('Parameter df not provided.')

        if (data_set is None or data_set == '') and ensure_cols:
            raise ValueError('Parameter data_set cannot be None or empty if ensure_cols is True.')

        dd = self.df(data_set)

        types_map = dd['Type'].to_dict()
        types_map = {col: typ for (col, typ) in types_map.items() if col in df.columns}  # Remove mapping for columns that are not present in data frame.

        # Map values of str columns.
        str_cols = [col for (col, typ) in types_map.items() if typ == 'str']
        df[str_cols] = df[str_cols].apply(lambda col: col.map(lambda val: val if isinstance(val, str) and val != '' else None))

        # Ensure that nan is represented as None so that column type conversion does not result in object types if nan is present.
        df = df.replace('', np.nan)

        # Map values of bool columns.
        bool_cols = [col for (col, typ) in types_map.items() if typ == 'bool']
        df[bool_cols] = df[bool_cols].apply(lambda col: col.map(lambda val: self.__str_to_bool(val)))

        # Treat bool and str separately 'cause all non-empty strings are converted to True.
        # Map values of non-bool, non-str columns using data type.
        no_bool_str_types_map = {col: typ for (col, typ) in types_map.items() if typ not in ['bool', 'str']}
        df = df.astype(no_bool_str_types_map, errors='ignore')

        columns_map = dd['Name'].to_dict()
        df = df.rename(columns=columns_map)
        df = self.reorder(df)

        if ensure_cols:
            df = self.ensure_cols(df, data_set=data_set)

        if strip_cols:
            df = self.strip_cols(df, data_set=data_set)

        return df

    @auto_reload
    def reorder(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reorders the given data frame based on the order of the matching entries in the data dictionary.

        Args:
            df: The data frame whose columns need to be reordered.

        Returns:
            The reordered data frame.
        """
        return df[[x for x in self._names if x in list(df.columns.values)]
                  + [x for x in list(df.columns.values) if x not in self._names]]

    @auto_reload
    def ensure_cols(self, df: pd.DataFrame, cols: list = None, data_set: str = None) -> pd.DataFrame:
        """
        Ensures that the columns from the given data set or the given columns names are present the resulting data frame. Missing columns are added at the end.

        Args:
            df: The data frame to add the missing columns (if any) to.
            data_set: The name of data set to use. If this value matches a value in the `Data Set` column of the data dictionary,
                then `Name` column is used to identify missing columns. If `dataset` is not specified, the values in `Name` column
                that have entries with empty `Data Set` are used.
            cols: The column names to ensure are present in the returned data frame.

        Returns:
            The data frame with missing columns added to the end.
        """
        if cols is not None and data_set is not None:
            raise ValueError('Either the cols or the data_set arguments can be provided but not both.')

        if cols is None:
            cols = list(self.df(data_set)['Name'].values)

        current_cols = list(df.columns.values)+list(df.index.names)
        missing_cols = [v for v in cols if v not in current_cols]
        return df.reindex(columns=(list(df.columns.values)+missing_cols))

    @auto_reload
    def strip_cols(self, df: pd.DataFrame, data_set: str = None, any_data_set: bool = False):
        """
        Removes all columns that are not in the given data set from the given data frame or all columns that are not in any data set. It leaves
        the index untouched.

        Args:
            df: The data frame to remove the columns from.
            data_set: The name of the data set with columns to preserve.
            any_data_set: Whether to remove all columns that are not in any data set.

        Returns:
            The data frame is only the data set columns.
        """
        if any_data_set and data_set is not None:
            raise ValueError('Either data_set can be provide or any_data_set can be True but not both.')

        ds_cols = list(self.df(data_set, any_data_set)['Name'].values)
        df_cols = [v for v in df.columns if v in ds_cols]
        return df[df_cols]

    @staticmethod
    def add_stats(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds the `Total` and `Average` of the column values as two rows at the top of the data frame.

        Args:
            df: The data frame to summarise.

        Returns:
            The data frame with the `Total` and `Average` at the top.
        """
        if df is None:
            raise ValueError('Parameter df is mandatory')

        num_agg_map = {col: DataDict.stats.keys() for col in df if is_numeric_dtype(df[col]) and df[col].dtype != np.bool}
        aggr_row = df.agg(num_agg_map).rename(DataDict.stats)
        if len(df.index.names) > 1:
            aggr_row = pd.concat([aggr_row], keys=[np.nan] * len(DataDict.stats.keys()), names=df.index.names[1:])
        df = pd.concat([df.iloc[:0], aggr_row, df], sort=False)

        # Adds the dictionary of stats to the data frame.
        if not hasattr(df, 'stats'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df.stats = {}

        df.stats = {**df.stats, **DataDict.stats}

        return df

    @staticmethod
    def has_stats(df: pd.DataFrame):
        """
        Checks whether the given data frame has stats rows added at the top of the data frame.

        Args:
            df: The data frame to check.

        Returns:
            Whether the given data frame has stats.
        """
        return hasattr(df, 'stats')

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the data frame based on the `Format` attribute in the data dictionary.

        Args:
            df: The data frame to format.

        Returns:
            The formatted data frame.
        """
        if df is None:
            raise ValueError('Parameter df is mandatory')

        # Necessary to define separate function instead of using lambda directly (see https://stackoverflow.com/questions/36805071/dictionary-comprehension-with-lambda-functions-gives-wrong-results)
        def make_func(f: str = None):
            def format_value(x):
                if f is None or f == '':
                    return x if not pd.isnull(x) else '-'

                return f.format(x) if not pd.isnull(x) else '-'

            # If mean is part of the stats, then the integer numbers need to be formatted as floats because the mean of integers can be float.
            if self.has_stats(df) and 'mean' in df.stats.keys() and f is not None:
                f = f.replace(':d', ':.1f')

            return lambda x: format_value(x)

        # Assembles a dictionary with columns as key and format functions as values but only for the columns that are actually in the data frame.
        formats = {col: make_func(f) for (col, f) in self._formats.items() if col in df.columns.values}
        formats = {**formats, **{col: make_func() for col in set(df.columns.values) - set(self._formats.keys())}}

        df = df.copy()
        for col, value in formats.items():
            try:
                df[col] = df[col].apply(value)
            except ValueError as e:
                warnings.warn(f'A value in column {col} could not be formatted.\nError message: {e}')

        return df

    def __hash__(self):
        """
        Calculates the hash value of the data dictionary by calculating the hash value of the data dictionary data frame.

        Returns:
            The hash value of the data dictionary.
        """
        return hash(pickle.dumps(self.data_dict))


DataDict.meta = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                          data={0: ['data_dict', 'data_set', 'Data Set', 'Used when mapping in combination with Field to rename to the column to Name.', 'str', '{:s}'],
                                                                1: ['data_dict', 'field', 'Field', 'Column name of the data frame to map to Name.', 'str', '{:s}'],
                                                                2: ['data_dict', 'name', 'Name', 'Column name that is unique throughout the data dictionary.', 'str', '{:s}'],
                                                                3: ['data_dict', 'description', 'Description', 'Description of the column name. This can be used to provide additional information when displaying the data frame.', 'str',
                                                                    '{:s}'],
                                                                4: ['data_dict', 'type', 'Type', 'Type the column should be cast to.', 'str', '{:s}'],
                                                                5: ['data_dict', 'format', 'Format',
                                                                    'Format to use when values need to be converted to a string representation. The format string has to be a Python format string such as {:.0f}%', 'str', '{:s}']},
                                                          columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))
