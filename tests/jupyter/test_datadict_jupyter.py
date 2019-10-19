import unittest
import unittest.mock as mock
import pandas as pd
import ipywidgets as widgets
from datadict.jupyter import DataDict


class TestDataDictJupyter(unittest.TestCase):
    def test_display(self):
        dd = DataDict(data_dict=pd.DataFrame.from_dict(orient='index',
                                                       data={0: ['data_set_1', 'field_1', 'Name 1', 'Description 1', 'str', ''],
                                                             1: ['data_set_1', 'field_2', 'Name 2', 'Description 2', 'int', '{:d}'],
                                                             2: ['data_set_1', 'field_3', 'Name 3', 'Description 3', 'bool', '{:}'],
                                                             3: ['data_set_1', 'field_4', 'Name 4', 'Description 4', 'float', '£{:.1f}m'],
                                                             4: ['data_set_1', 'field_5', 'Name 5', 'Description 5', 'datetime64', '']},

                                                       columns=['Data Set', 'Field', 'Name', 'Description', 'Type', 'Format']))
        data = [{'field_1': 'test 1', 'field_2': '1', 'field_3': 'True', 'field_4': '1.1', 'field_5': '2019-01-01', 'field_6': 'bayern', },
                {'field_1': 'test 2', 'field_2': '2', 'field_3': 'FALSE', 'field_4': '1.2', 'field_5': '2019-01-02', 'field_6': 'bayern'},
                {'field_1': 'test 3', 'field_2': '3', 'field_3': '', 'field_4': '', 'field_5': '', 'field_6': 'bayern'}]

        df = pd.DataFrame.from_records(data)

        out = dd.display(df)
        self.assertIsInstance(out, widgets.VBox)
        self.assertIsInstance(out.children[0], widgets.Output)
        self.assertIsInstance(out.children[1], widgets.HBox)
        self.assertIsInstance(out.children[1].children[0], widgets.HTML)
        self.assertEqual(out.children[1].children[0].value, '3 rows x 6 columns')
        self.assertIsInstance(out.children[2], widgets.Accordion)


