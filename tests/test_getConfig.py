
import unittest
import os
from unittest.mock import patch, mock_open
import src.getConfig as getConfig
import yaml


class TestGetConfig(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="db_user: test_user\ndb_password: test_password")
    @patch("os.path.abspath", return_value="../config/config.yaml")
    def test_get_config(self, mock_file):
        # Test for existing key
        result = getConfig.get_config("db_user")
        self.assertEqual(result, "test_user")

        # Ensure the file was opened correctly
        mock_file.assert_called_once_with("../config/config.yaml", "r")

        # Test for non-existing key
        result = getConfig.get_config("non_existing_key")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()