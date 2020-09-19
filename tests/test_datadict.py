import unittest
import os
from datadict import DataDict
import logging as log
import pandas as pd
from pandas.util.testing import assert_frame_equal
from datetime import datetime
import numpy as np

log.basicConfig(level=log.INFO, format='%(message)s')


class TestDataDict(unittest.TestCase):
    dd: DataDict = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                             data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                                   1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                                   2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                                   3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
                                                                   4: ['data_set_1', 'field_5', 'Name 5', 'Description 5', 'datetime64', '{:%B %d, %Y}']},
                                                             columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                      'Format']))

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

        data_dict_file = os.path.join(os.path.dirname(__file__), 'data_dict.csv')
        actual_dd = DataDict(data_dict_file=data_dict_file)

        assert_frame_equal(expected_dd.data_dict, actual_dd.data_dict)

    def test_data_set_df(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))
        actual_df = dd.df('data_set_1')

        expected = {0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', '']}
        expected_df = (pd.DataFrame.from_dict(expected, orient='index',
                                              columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']) \
                       .set_index('Field'))

        assert_frame_equal(expected_df, actual_df)

    def test_data_set_df_none(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))
        actual_df = dd.df()

        expected = {1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']}
        expected_df = (pd.DataFrame.from_dict(expected, orient='index',
                                              columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']) \
                       .set_index('Field'))

        assert_frame_equal(expected_df, actual_df)

    def test_data_set_df_empty(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))
        actual_df = dd.df('')

        expected = {1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']}
        expected_df = (pd.DataFrame.from_dict(expected, orient='index',
                                              columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']) \
                       .set_index('Field'))

        assert_frame_equal(expected_df, actual_df)

    def test_data_set_df_any_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))
        actual_df = dd.df(any_data_set=True)

        expected = {0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                    1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']}
        expected_df = (pd.DataFrame.from_dict(expected, orient='index',
                                              columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']) \
                       .set_index('Field'))

        assert_frame_equal(expected_df, actual_df)

    def test_data_set_df_data_set_any_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))

        with self.assertRaisesRegex(ValueError, f'Either data_set can be provide or any_data_set can be True but not both.'):
            dd.df(data_set='data_set_1', any_data_set=True)


    def test_remap(self):
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
        actual_df = self.dd.remap(df, 'data_set_1')

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

    def test_remap_empty_df(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=[])

        df = pd.DataFrame.from_dict({}, orient='index', columns=[])
        actual_df = dd.remap(df, 'data_set_1')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_remap_empty_df_ensure_columns(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['field_1'])
        actual_df = dd.remap(df, 'data_set_1', True)
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_remap_empty_df_ensure_columns_none_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        df = pd.DataFrame.from_dict({}, orient='index', columns=[])
        with self.assertRaises(ValueError):
            dd.remap(df, None, True)

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

        data = [{'field_5': 'bayern', 'field_2': '1', 'field_1': 'test 1', 'field_3': 'True', 'field_4': '1.1', }]

        df = pd.DataFrame.from_records(data)
        actual_df = dd.remap(df, 'data_set_1')

        assert_frame_equal(expected_df, actual_df)

    def test_ensure_cols_df_additional_cols(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 2', 'Name 1'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 2'])
        actual_df = dd.ensure_cols(df, cols=['Name 1'])
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_ensure_cols_df_additional_cols(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1', 'Name 2'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=[])
        actual_df = dd.ensure_cols(df, cols=['Name 1', 'Name 2'])
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_ensure_cols_df_overlapping_cols(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1', 'Name 2'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1', 'Name 2'])
        actual_df = dd.ensure_cols(df, cols=['Name 2', 'Name 1'])
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_ensure_cols_df_additional_cols_ds(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 2', 'Name 1'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 2'])
        actual_df = dd.ensure_cols(df, data_set='data_set_1')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_ensure_cols_df_overlapping_cols_ds(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        data = {0: ['test 1', 1]}
        expected_df = pd.DataFrame.from_dict(data, orient='index', columns=['Name 1', 'Name 2'])

        actual_df = pd.DataFrame.from_dict(data, orient='index', columns=['Name 1', 'Name 2'])
        actual_df = dd.ensure_cols(actual_df, data_set='data_set_1')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_ensure_cols_df_no_cols_ds(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1'])

        df = pd.DataFrame.from_dict({}, orient='index', columns=[])
        actual_df = dd.ensure_cols(df, data_set='data_set_1')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_ensure_cols_df_index_cols_ds(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        expected_df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1', 'Name 2']).set_index('Name 1')

        df = pd.DataFrame.from_dict({}, orient='index', columns=['Name 1']).set_index('Name 1')
        actual_df = dd.ensure_cols(df, data_set='data_set_1')
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_strip_cols(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        df = pd.DataFrame.from_records([{'Name 1': 'test 1', 'Name 2': '1', 'Name 3': 'True'}])
        actual_df = dd.strip_cols(df, data_set='data_set_1')

        expected_df = pd.DataFrame.from_records([{'Name 1': 'test 1'}])
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_strip_cols_any_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        df = pd.DataFrame.from_records([{'Name 1': 'test 1', 'Name 2': '1', 'Name 3': 'True'}])
        actual_df = dd.strip_cols(df, any_data_set=True)

        expected_df = pd.DataFrame.from_records([{'Name 1': 'test 1', 'Name 2': '1'}])
        assert_frame_equal(expected_df, actual_df, check_dtype=False)

    def test_strip_cols_data_set_and_any_data_set(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['', 'field_1', 'Name 2', 'Description 2', 'int', '{:d}']},
                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type',
                                                                'Format']))

        df = pd.DataFrame.from_records([{'Name 1': 'test 1', 'Name 2': '1', 'Name 3': 'True'}])
        with self.assertRaisesRegex(ValueError, f'Either data_set can be provide or any_data_set can be True but not both.'):
            dd.strip_cols(df, data_set='data_set_1', any_data_set=True)

    def test_has_stats_with_stats(self):
        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern', }]
        df = pd.DataFrame.from_records(data)
        df = self.dd.add_stats(df)

        self.assertTrue(self.dd.has_stats(df))

    def test_has_stats_without_stats(self):
        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern', }]
        df = pd.DataFrame.from_records(data)

        self.assertFalse(self.dd.has_stats(df))

    def test_add_stats(self):
        expected = {'Total': [np.nan, 10.0, np.nan, 2.3, np.nan, np.nan],
                    'Average': [np.nan, 2.5, np.nan, 1.15, np.nan, np.nan],
                    0: ['test 1', 1.0, True, 1.1, datetime(2019, 1, 1), 'bayern'],
                    1: ['test 2', 2.0, False, 1.2, datetime(2019, 1, 2), 'bayern'],
                    2: ['test 3', 3.0, np.nan, None, None, 'bayern'],
                    3: ['test 4', 4.0, np.nan, None, None, 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5', 'field_6'])
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'float', 'Name 4': 'float', 'Name 5': 'datetime64', 'field_6': 'str'},
                                         errors='ignore')
        expected_df = expected_df.replace('nan', np.nan)

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 2', 'field_2': '2', 'field_3': 'FALSE', 'field_4': '1.2', 'field_5': '2019-01-02', 'field_6': 'bayern'},
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'},
                {'field_1': 'test 4', 'field_2': '4', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'}]

        df = pd.DataFrame.from_records(data)
        actual_df = self.dd.remap(df, 'data_set_1')
        actual_df = self.dd.add_stats(actual_df)

        assert_frame_equal(expected_df, actual_df, check_dtype=False)
        self.assertEqual({'sum': 'Total', 'mean': 'Average'}, actual_df.stats)

    def test_add_stats_with_multi_index(self):
        expected = [{'Name 1': np.nan, 'Name 2': 'Total', 'Name 3': np.nan, 'Name 4': 2.3, 'Name 5': np.nan, 'field_6': np.nan, },
                    {'Name 1': np.nan, 'Name 2': 'Average', 'Name 3': np.nan, 'Name 4': 1.15, 'Name 5': np.nan, 'field_6': np.nan, },
                    {'Name 1': 'test 1', 'Name 2': 1, 'Name 3': True, 'Name 4': '1.1', 'Name 5': '2019-01-01', 'field_6': 'bayern', },
                    {'Name 1': 'test 2', 'Name 2': 2, 'Name 3': False, 'Name 4': '1.2', 'Name 5': '2019-01-02', 'field_6': 'bayern'},
                    {'Name 1': 'test 3', 'Name 2': 3, 'Name 3': np.nan, 'Name 4': np.nan, 'Name 5': np.nan, 'field_6': 'bayern'},
                    {'Name 1': 'test 4', 'Name 2': 4, 'Name 3': np.nan, 'Name 4': np.nan, 'Name 5': np.nan, 'field_6': 'bayern'}]

        expected_df = pd.DataFrame.from_records(expected)
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'float', 'Name 4': 'float', 'Name 5': 'datetime64', 'field_6': 'str'},
                                         errors='ignore')
        expected_df = expected_df.replace('nan', np.nan).set_index(['Name 1', 'Name 2'])

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 2', 'field_2': '2', 'field_3': 'FALSE', 'field_4': '1.2', 'field_5': '2019-01-02', 'field_6': 'bayern'},
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'},
                {'field_1': 'test 4', 'field_2': '4', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'}]

        df = pd.DataFrame.from_records(data)
        actual_df = self.dd.remap(df, 'data_set_1').set_index(['Name 1', 'Name 2'])
        actual_df = self.dd.add_stats(actual_df)

        assert_frame_equal(expected_df, actual_df, check_dtype=False)
        self.assertEqual({'sum': 'Total', 'mean': 'Average'}, actual_df.stats)

    def test_format(self):
        expected = {0: ['test 1', '1', 'True', '£1.1m', 'January 01, 2019', 'bayern'],
                    1: ['test 3', '3', '-', '-', '-', 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5', 'field_6'])
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'str', 'Name 3': 'str', 'Name 4': 'str', 'Name 5': 'datetime64', 'field_6': 'str'},
                                         errors='ignore')

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern', }]
        df = pd.DataFrame.from_records(data)

        actual_df = self.dd.remap(df, 'data_set_1')
        actual_df = self.dd.format(actual_df)
        self.maxDiff = None
        assert_frame_equal(expected_df, actual_df)

    def test_format_unmapped_cols(self):
        expected = {0: ['test 1', 1, 1.0, True, datetime(2019, 1, 1), '-'],
                    1: ['test 3', 3, 3.0, False, datetime(2019, 1, 3), '-']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6'])

        data = [{'field_1': 'test 1', 'field_2': 1, 'field_3': 1.0, 'field_4': True, 'field_5': datetime(2019, 1, 1), 'field_6': None, },
                {'field_1': 'test 3', 'field_2': 3, 'field_3': 3.0, 'field_4': False, 'field_5': datetime(2019, 1, 3), 'field_6': None, }]
        df = pd.DataFrame.from_records(data)

        actual_df = self.dd.format(df)
        self.maxDiff = None

        assert_frame_equal(expected_df, actual_df)

    def test_format_with_stats(self):
        expected = {'Total': ['-', '3.0', '-', '£1.1m', '-', '-'],
                    'Average': ['-', '1.5', '-', '£1.1m', '-', '-'],
                    0: ['test 1', '1.0', 'True', '£1.1m', 'January 01, 2019', 'bayern'],
                    1: ['test 3', '2.0', 'False', '-', '-', 'bayern']}
        expected_df = pd.DataFrame.from_dict(expected, orient='index',
                                             columns=['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 5', 'field_6'])
        expected_df = expected_df.astype({'Name 1': 'str', 'Name 2': 'str', 'Name 3': 'str', 'Name 4': 'str', 'Name 5': 'datetime64', 'field_6': 'str'},
                                         errors='ignore')

        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 3', 'field_2': '2', 'field_3': 'False', 'field_4': '', 'field_5': '', 'field_6': 'bayern', }]

        df = pd.DataFrame.from_records(data)
        actual_df = self.dd.remap(df, 'data_set_1')
        actual_df = self.dd.add_stats(actual_df)
        actual_df = self.dd.format(actual_df)
        self.maxDiff = None
        assert_frame_equal(expected_df, actual_df)

    def test_meta(self):
        # Tests that the meta data dictionary is a valid data dictionary.
        DataDict.validate(DataDict.meta.data_dict)

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
