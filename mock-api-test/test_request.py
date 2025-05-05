import unittest
from unittest.mock import patch
from request_user import get_user_data
 
class TestGetUserData(unittest.TestCase):
 
    @patch('requests.get')
    def test_get_user_data_success(self, mock_get):
        # Mengatur mock response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "John Doe"}
        
        # Set mock object as the return value of requests.get
        mock_get.return_value = mock_response
        
        # Menguji fungsi
        user_data = get_user_data(1)
        
        # Melakukan assertion pada nilai yang dikembalikan fungsi.
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["id"], 1)
        self.assertEqual(user_data["name"], "John Doe")
 
    @patch('requests.get')
    def test_get_user_data_failure(self, mock_get):
        # Mengatur mock response jika gagal.
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Menguji fungsi
        user_data = get_user_data(1)
        
       # Melakukan assertion pada nilai yang dikembalikan fungsi.
        self.assertIsNone(user_data)
    
    @patch('requests.get', side_effect=TimeoutError)      # Kode Baru
    def test_timeout_error(self, mock_get):        # Kode Baru
        with self.assertRaises(TimeoutError):        # Kode Baru
            get_user_data(1)                    # Kode Baru
 
 
if __name__ == "__main__":
    unittest.main()