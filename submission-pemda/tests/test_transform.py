import unittest
import os
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            ['Unknown Product', '$100.00', 'Invalid Rating / 5', '5 Colors', 'Size: M', 'Gender: Men', '2025-05-09 15:30:01'],
            ['T-shirt 2', '$102.15', '⭐ 3.9 / 5', '3 Colors', 'Size: M', 'Gender: Women', '2025-05-09 15:30:01'],
        ]
        
        self.test_file = 'test_products.csv'
        
        header = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        df = pd.DataFrame(self.test_data, columns=header)
        df.to_csv(self.test_file, index=False)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_transform_data(self):
        transformed_df = transform_data(self.test_file)


        self.assertEqual(len(transformed_df), 1)

        self.assertEqual(transformed_df['Price'].iloc[0], 1634400.0)  

        self.assertEqual(transformed_df['Rating'].iloc[0], 3.9)  

        self.assertEqual(transformed_df['Colors'].iloc[0], 3) 

        self.assertEqual(transformed_df['Size'].iloc[0], 'M') 

        self.assertEqual(transformed_df['Gender'].iloc[0], 'Women') 

        self.assertTrue(transformed_df['Timestamp'].iloc[0].endswith('Z')) 

    def test_invalid_rating_removed(self):
        transformed_df = transform_data(self.test_file)
        
        self.assertNotIn('Unknown Product', transformed_df['Title'].values)

    def test_invalid_price_removed(self):
        transformed_df = transform_data(self.test_file)
        
        self.assertNotIn('Price Unavailable', transformed_df['Price'].values)

if __name__ == '__main__':
    unittest.main()
