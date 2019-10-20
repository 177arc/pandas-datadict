import pandas as pd
import numpy as np
import os
from pandas.api.types import is_numeric_dtype
from os import path
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
    meta = None

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
        if not data_dict_file is None and not data_dict is None:
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

        if not data_dict is None:
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

    def __str_to_bool(self, value: str) -> object:
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

    def remap(self, df: pd.DataFrame, data_set: str = None) -> pd.DataFrame:
        """
        Renames the columns in the given data frame based on based on the `Data Set` and `Field` attributes in the data dictionary to `Name`
        if such a mapping found and converts the columns data to `Type`. It also reorders the columns based on the order of the data dictionary entries.

        Args:
            df: The data frame to remap.
            data_set: The data set to use. If this value matches a value in the `Data Set` column of the data dictionary, then the corresponding names in the `Field`
                column are used to rename the columns of the given data frame to the `Name` column name. If `dataset` is not specified, the values in `Field` column
                that have entries with empty `Data Set` are used.

        Returns:
            The remapped data frame.
        """
        if self.auto_reload:
            self.__load()

        if df is None:
            raise ValueError('Parameter df not provided..')

        if data_set is None:
            data_set = ''

        dd = self._data_dict[self._data_dict['Data Set'] == data_set].set_index('Field')

        # Ensure that nan is represented as None so that column type conversion does not result in object types if nan is present.
        df = df.replace('', np.nan)

        types_map = dd['Type'].to_dict()
        types_map = {col: type for (col, type) in types_map.items() if col in df.columns}  # Remove mapping for columns that are not present in data frame,

        # Treat with bool separately 'cause all non-empty strings are converted to True.
        # Map values of non-bool columns using data type.
        no_bool_types_map = {col: type for (col, type) in types_map.items() if type != 'bool'}
        df = df.astype(no_bool_types_map, errors='ignore')

        # Map values of bool columns using data type.
        bool_cols = [col for (col, type) in types_map.items() if type == 'bool']
        df[bool_cols] = df[bool_cols].apply(lambda col: col.map(lambda val: self.__str_to_bool(val)))

        columns_map = dd['Name'].to_dict()
        df = df.rename(columns=columns_map)
        df = self.reorder(df)
        return df

    def reorder(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reorders the given data frame based on the order of the matching entries in the data dictionary.

        Args:
            df: The data frame whose columns need to be reordered.

        Returns:
            The reordered data frame.
        """
        if self.auto_reload:
            self.__load()

        return df[[x for x in self._names if x in list(df.columns.values)] + [x for x in list(df.columns.values) if
                                                                              x not in self._names]]

    def add_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds the `Total` and `Average` of the column values as two rows at the top of the data frame.

        Args:
            df: The data frame to summarise.

        Returns:
            The data frame with the `Total` and `Average` at the top.
        """
        if df is None: raise ValueError('Parameter df is mandatory')
        num_agg_map = {col: ['sum', 'mean'] for col in df if is_numeric_dtype(df[col])}
        func_map = {'sum': 'Total', 'mean': 'Average'}
        aggr_row = df.agg(num_agg_map).rename(func_map)
        df = pd.concat([df.iloc[:0], aggr_row, df], sort=False)

        return df

    def format(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the data frame based on the `Format` attribute in the data dictionary.

        Args:
            df: The data frame to format.

        Returns:
            The formatted data frame.
        """
        if df is None: raise ValueError('Parameter df is mandatory')

        # Necessary to define separate function instead of using lambda directly (see https://stackoverflow.com/questions/36805071/dictionary-comprehension-with-lambda-functions-gives-wrong-results)
        def make_func(f):
            return lambda x: f.format(x) if not pd.isnull(x) else '-' \
                                                                  ''

        formats = {col: make_func(f) for (col, f) in self._formats.items()}

        df = df.copy()
        for col, value in formats.items():
            if col in df.columns:
                df[col] = df[col].apply(value)

        return df

DataDict.meta = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
             data={0: ['data_dict', 'data_set', 'Data Set', 'Used when mapping in combination with Field to rename to the column to Name.', 'str', '{:s}'],
                   1: ['data_dict', 'field', 'Field', 'Column name of the data frame to map to Name.', 'str', '{:s}'],
                   2: ['data_dict', 'name', 'Name', 'Column name that is unique throughout the data dictionary.', 'str', '{:s}'],
                   3: ['data_dict', 'description', 'Description', 'Description of the column name. This can be used to provide additional information when displaying the data frame.', 'str', '{:s}'],
                   4: ['data_dict', 'type', 'Type', 'Type the column should be cast to.', 'str', '{:s}'],
                   5: ['data_dict', 'format', 'Format', 'Format to use when values need to be converted to a string representation. The format string has to be a Python format string such as {:.0f}%', 'str', '{:s}']},
             columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))