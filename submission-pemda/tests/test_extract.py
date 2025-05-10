import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import extract_data, process_page, save_to_csv
from datetime import datetime
import os
import csv

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_extract_data_first_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">
                        <span class="price">$100.00</span>
                    </div>
                    <div class="product-details">
                        <p>Rating: ⭐ 4.5 / 5</p>
                        <p>5 Colors</p>
                        <p>Size: M</p>
                        <p>Gender: Men</p>
                    </div>
                </div>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        data = []
        extraction_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        soup = BeautifulSoup(mock_response.text, 'html.parser')
        process_page(soup, data, extraction_timestamp)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], [
            'Test Product',
            '$100.00',
            'Rating: ⭐ 4.5 / 5',
            '5 Colors',
            'Size: M',
            'Gender: Men',
            extraction_timestamp
        ])

    @patch('utils.extract.csv.writer')
    def test_save_to_csv(self, mock_csv_writer):
        data = [['Test Product', '$100.00', 'Rating: ⭐ 4.5 / 5', '5 Colors', 'Size: M', 'Gender: Men', '2025-05-09 15:30:01']]
        
        save_to_csv(data)

        mock_csv_writer.assert_called_once()
        args, kwargs = mock_csv_writer.call_args
        
        self.assertTrue('products.csv' in args[0].name)

    def test_csv_content(self):
        data = [['Test Product', '$100.00', 'Rating: ⭐ 4.5 / 5', '5 Colors', 'Size: M', 'Gender: Men', '2025-05-09 15:30:01']]
        
        save_to_csv(data)

        output_path = os.path.join(os.getcwd(), 'products.csv')
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            lines = list(reader)

        self.assertEqual(lines[0], ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp'])
        self.assertEqual(lines[1], ['Test Product', '$100.00', 'Rating: ⭐ 4.5 / 5', '5 Colors', 'Size: M', 'Gender: Men', '2025-05-09 15:30:01'])


if __name__ == '__main__':
    unittest.main()
