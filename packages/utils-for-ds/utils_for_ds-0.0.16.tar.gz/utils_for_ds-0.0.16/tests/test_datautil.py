import unittest

from utils_for_ds.data_utils import create_date_df
import pandas as pd
from datetime import datetime

class TestCaseCresteDateDf(unittest.TestCase):
    def test_create_date_df(self):
        df = create_date_df()
        data = { 'DATE' : [datetime.strptime('20210101', '%Y%m%d')]}
        df_result = pd.DataFrame(data)
        bool_result = (df==df_result).all()
        self.assertEqual(bool_result['DATE'], True)

    def test_create_date_df_error_input(self):
        df = create_date_df('20220102', '20220101')
        self.assertEqual(df, False)