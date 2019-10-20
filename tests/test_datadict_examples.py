import unittest

import pandas as pd
from datetime import datetime
from datadict import DataDict

class TestDataDictExamples(unittest.TestCase):

    def test_example_load_file_remap(self):
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


    def test_example_df_remap(self):
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