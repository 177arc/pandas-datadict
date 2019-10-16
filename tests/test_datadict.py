import unittest
from datadict.datadict import DataDict
import logging as log
import pandas as pd
from pandas.util.testing import assert_frame_equal
from datetime import datetime
import numpy as np

log.basicConfig(level=log.INFO, format='%(message)s')


class TestDataDic(unittest.TestCase):
    def test_file_and_data_frame(self):
        with self.assertRaisesRegex(ValueError, 'data_dict_file.+data_dict'):
            DataDict(data_dict_file='data_dict.csv', data_dict=pd.DataFrame())

    def test_file_does_not_exist(self):
        with self.assertRaisesRegex(ValueError, 'The data dictionary file data_dict_imaginary.csv does not exist'):
            DataDict(data_dict_file='data_dict_imaginary.csv')

    def test_file(self):
        expected_df = pd.DataFrame.from_dict(orient='index',
                                             data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                   1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                   2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                   3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
                                                   4: ['data_set_2', 'field_1', 'Name 21', 'Description 1', 'str', ''],
                                                   5: ['', '', 'Name 22', 'Description 2', 'int', '{:d}']},
                                             columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format'])
        expected_df = expected_df.replace('', np.nan)
        expected_dd = DataDict(data_dict=expected_df)

        actual_dd = DataDict(data_dict_file='data_dict.csv')

        assert_frame_equal(expected_dd.data_dict, actual_dd.data_dict)

    def test_remap(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
                                                             4: ['data_set_1', 'field_5', 'Name 5', 'Description 5', 'datetime64', '']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

        expected = {0: ['test 1', 1, True, 1.1, datetime(2019, 1, 1), 'bayern'],
                    1: ['test 2', 2, False, 1.2, datetime(2019, 1, 2), 'bayern'],
                    2: ['test 3', 3, np.nan, None, None, 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5', 'field_6'])
        expected_df['Name 4'] = expected_df['Name 4'].astype('float')
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'int', 'Name 4': 'float', 'Name 5': 'datetime64', 'field_6': 'str'},
                                         errors='ignore')

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 2', 'field_2': '2', 'field_3': 'FALSE', 'field_4': '1.2', 'field_5': '2019-01-02', 'field_6': 'bayern'},
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'}]

        df = pd.DataFrame.from_records(data)
        actual_df = dd.remap(df, 'data_set_1')

        assert_frame_equal(expected_df, actual_df)

    def test_remap_empty_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 2'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['field_1'])
        actual_df = dd.remap(df, '')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_remap_none_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 2'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['field_1'])
        actual_df = dd.remap(df, None)
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_remap_none_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', '']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['field_2'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['field_2'])
        actual_df = dd.remap(df, 'data_set_1')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_remap_reorder(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected = {0: ['test 1', 1, True, 1.1, 'bayern'],
                    1: ['test 2', 2, False, 1.2, 'bayern'],
                    2: ['test 3', 3, np.nan, None, 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'field_5'])
        expected_df['Name 4'] = expected_df['Name 4'].astype('float')
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'int', 'Name 4': 'float', 'field_5': 'str'},
                                         errors='ignore')

        data = [{'field_5': 'bayern', 'field_2': '1', 'field_1': 'test 1', 'field_3': 'True', 'field_4': '1.1', },
                {'field_5': 'bayern', 'field_2': '2', 'field_1': 'test 2', 'field_3': 'FALSE', 'field_4': '1.2', },
                {'field_5': 'bayern', 'field_2': '3', 'field_1': 'test 3', 'field_3': '', 'field_4': '', }]

        df = pd.DataFrame.from_records(data)
        actual_df = dd.remap(df, 'data_set_1')

        assert_frame_equal(expected_df, actual_df)

    def test_reorder(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected = {0: ['test 1', 1, True, 1.1, 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'field_5'])
        expected_df['Name 4'] = expected_df['Name 4'].astype('float')
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'int', 'Name 4': 'float', 'field_5': 'str'},
                                         errors='ignore')

        data = [{'field_5': 'bayern', 'field_2': '1', 'field_1': 'test 1', 'field_3': 'True', 'field_4': '1.1',}]

        df = pd.DataFrame.from_records(data)
        actual_df = dd.remap(df, 'data_set_1')

        assert_frame_equal(expected_df, actual_df)

    def test_add_stats(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
                                                             4: ['data_set_1', 'field_5', 'Name 5', 'Description 5', 'datetime64', '']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected = {'Total': [np.nan, 6, np.nan, 2.3, np.nan, np.nan],
                    'Average': [np.nan, 2, np.nan, 1.15, np.nan, np.nan],
                    0: ['test 1', 1, True, 1.1, datetime(2019, 1, 1), 'bayern'],
                    1: ['test 2', 2, False, 1.2, datetime(2019, 1, 2), 'bayern'],
                    2: ['test 3', 3, np.nan, None, None, 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5', 'field_6'])
        expected_df['Name 4'] = expected_df['Name 4'].astype('float')
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'int', 'Name 4': 'float', 'Name 5': 'datetime64', 'field_6': 'str'},
                                         errors='ignore')
        expected_df = expected_df.replace('nan', np.nan)

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 2', 'field_2': '2', 'field_3': 'FALSE', 'field_4': '1.2', 'field_5': '2019-01-02', 'field_6': 'bayern'},
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'}]

        df = pd.DataFrame.from_records(data)
        actual_df = dd.add_stats(dd.remap(df, 'data_set_1'))

        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_format(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', '{:s}'],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected = {0: ['test 1', '1', 'True', '£1.1m', 'bayern'],
                    1: ['test 3', '3', '-', '-', 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'field_5'])
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'str', 'Name 3': 'str', 'Name 4': 'str', 'field_5': 'str'},
                                         errors='ignore')

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': 'bayern', },
                { 'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': 'bayern', }]

        df = pd.DataFrame.from_records(data)
        actual_df = dd.remap(df, 'data_set_1')
        actual_df = dd.format(actual_df)
        self.maxDiff = None
        assert_frame_equal(expected_df, actual_df)

    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError, f'{DataDict.column_names}'):
            DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                      data={
                                                          0: ['data_set_1']},
                                                      columns=['Data Set']))

    def test_non_unique_names(self):
        with self.assertRaisesRegex(ValueError, f'\'Name 1\'.+unique'):
            DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                      data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                            1: ['data_set_1', 'field_2', 'Name 1', 'Description 2', 'int', '{:d}'],
                                                            2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}']},
                                                      columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

    def test_non_field_id(self):
        with self.assertRaisesRegex(ValueError, f'\'data_set_1\.field_1\'.+unique'):
            DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                      data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                            1: ['data_set_1', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                            2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}']},
                                                      columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

    def test_invalid_type(self):
        with self.assertRaisesRegex(ValueError, f'{DataDict.supported_types}'):
            DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                      data={
                                                          0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str1', '']},
                                                      columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

    def test_multiple_no_data_set_no_field(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', '', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['', '', 'Name 3', 'Description 3', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        self.assertTrue(True)

