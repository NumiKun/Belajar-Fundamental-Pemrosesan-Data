import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from sqlalchemy import create_engine
import gspread
from utils.load import load_data_to_postgresql, load_data_to_google_sheets, save_to_postgresql_and_sheets
from datetime import datetime

class TestLoadFunctions(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            'Title': ['T-shirt 2', 'Hoodie 3', 'Pants 4', 'Outerwear 5', 'Jacket 6'],
            'Price': [1634400.0, 7950080.0, 7476960.0, 5145440.0, 2453920.0],
            'Rating': [3.9, 4.8, 3.3, 3.5, 3.3],
            'Colors': [3, 3, 3, 3, 3],
            'Size': ['M', 'L', 'XL', 'XXL', 'S'],
            'Gender': ['Women', 'Unisex', 'Men', 'Women', 'Unisex'],
            'Timestamp': ['2025-05-09T22:35:34Z'] * 5
        }
        self.sample_df = pd.DataFrame(self.sample_data)
        self.test_db_url = 'postgresql://surya:surya2003@localhost:5432/submissiondb'
        self.test_spreadsheet_id = '1xTuV-oBslKY0l83Ua0xgDLt3zMm92SnKzxHJ9QalcEU'
        self.test_sheet_name = 'Sheet1'

    def test_dataframe_structure(self):
        expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        self.assertListEqual(list(self.sample_df.columns), expected_columns)
        self.assertEqual(self.sample_df['Price'].dtype, 'float64')
        self.assertEqual(self.sample_df['Rating'].dtype, 'float64')
        self.assertEqual(self.sample_df['Colors'].dtype, 'int64')
        self.assertEqual(self.sample_df['Size'].dtype, 'object')
        self.assertEqual(self.sample_df['Gender'].dtype, 'object')
        self.assertEqual(self.sample_df['Timestamp'].dtype, 'object')

    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_load_data_to_postgresql_with_sample_data(self, mock_to_sql, mock_engine):
        mock_engine_instance = MagicMock()
        mock_engine.return_value = mock_engine_instance
        load_data_to_postgresql(self.sample_df, self.test_db_url)
        mock_engine.assert_called_once_with(self.test_db_url)
        mock_to_sql.assert_called_once()
        call_args = mock_to_sql.call_args
        self.assertEqual(call_args[0][0], 'products')
        self.assertEqual(call_args[0][1], mock_engine_instance)
        self.assertEqual(call_args[1]['if_exists'], 'replace')
        self.assertEqual(call_args[1]['index'], False)
        mock_engine_instance.dispose.assert_called_once()

    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    @patch('utils.load.gspread.authorize')
    def test_load_data_to_google_sheets_with_sample_data(self, mock_authorize, mock_credentials):
        mock_client = MagicMock()
        mock_authorize.return_value = mock_client
        mock_sheet = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_spreadsheet.worksheet.return_value = mock_sheet
        mock_client.open_by_key.return_value = mock_spreadsheet
        load_data_to_google_sheets(self.sample_df, self.test_spreadsheet_id, self.test_sheet_name)
        mock_credentials.assert_called_once()
        mock_authorize.assert_called_once()
        mock_client.open_by_key.assert_called_once_with(self.test_spreadsheet_id)
        mock_spreadsheet.worksheet.assert_called_once_with(self.test_sheet_name)
        mock_sheet.clear.assert_called_once()
        mock_sheet.update.assert_called_once_with([
            ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'],
            ['T-shirt 2', 1634400.0, 3.9, 3, 'M', 'Women', '2025-05-09T22:35:34Z'],
            ['Hoodie 3', 7950080.0, 4.8, 3, 'L', 'Unisex', '2025-05-09T22:35:34Z'],
            ['Pants 4', 7476960.0, 3.3, 3, 'XL', 'Men', '2025-05-09T22:35:34Z'],
            ['Outerwear 5', 5145440.0, 3.5, 3, 'XXL', 'Women', '2025-05-09T22:35:34Z'],
            ['Jacket 6', 2453920.0, 3.3, 3, 'S', 'Unisex', '2025-05-09T22:35:34Z']
        ])

    def test_data_integrity(self):
        original_data = self.sample_df.copy()
        with patch('utils.load.create_engine'):
            load_data_to_postgresql(self.sample_df, self.test_db_url)
            pd.testing.assert_frame_equal(self.sample_df, original_data)
        with patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name'), \
             patch('utils.load.gspread.authorize'):
            load_data_to_google_sheets(self.sample_df, self.test_spreadsheet_id, self.test_sheet_name)
            pd.testing.assert_frame_equal(self.sample_df, original_data)

    @patch('utils.load.load_data_to_postgresql')
    @patch('utils.load.load_data_to_google_sheets')
    def test_save_to_both_with_sample_data(self, mock_load_sheets, mock_load_postgres):
        save_to_postgresql_and_sheets(
            self.sample_df, 
            db_url=self.test_db_url,
            spreadsheet_name=self.test_spreadsheet_id,
            sheet_name=self.test_sheet_name
        )
        mock_load_postgres.assert_called_once_with(self.sample_df, self.test_db_url)
        mock_load_sheets.assert_called_once_with(self.sample_df, self.test_spreadsheet_id, self.test_sheet_name)

    def test_timestamp_handling(self):
        timestamps = pd.to_datetime(self.sample_df['Timestamp'])
        self.assertTrue(all(isinstance(ts, datetime) for ts in timestamps))
        self.assertTrue(all(ts.year == 2025 and ts.month == 5 and ts.day == 9 for ts in timestamps))

if __name__ == '__main__':
    unittest.main()