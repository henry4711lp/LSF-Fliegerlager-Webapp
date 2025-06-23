import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestMain(unittest.TestCase):

    def test_get_uid_from_cookie(self):
        with patch('getConfig.get_config', return_value='test'):
            import src.main as main
        with patch('src.main.request', new=MagicMock()) as mock_request:
            mock_request.cookies.get.return_value = '42'
            result = main.get_uid_from_cookie()
            self.assertEqual(result, '42')
            mock_request.cookies.get.assert_called_once_with('UserID')


if __name__ == '__main__':
    unittest.main()
