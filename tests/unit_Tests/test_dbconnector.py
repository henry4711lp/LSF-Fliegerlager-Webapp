import unittest
from unittest.mock import patch, MagicMock
import src.dbconnector as dbconnector
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))


class TestDBConnector(unittest.TestCase):

    @patch('getConfig.get_config')
    @patch('src.dbconnector.mysql.connector.connect')
    def test_sql(self, mock_connect, mock_get_config):
        # Mock the database connection and cursor
        mock_cnx = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_cnx
        mock_cnx.is_connected.return_value = True
        mock_cnx.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]
        mock_get_config.return_value = 'test'

        # SQL statement to be tested
        sql_statement = "SELECT * FROM test_table"

        # Call the function
        result = dbconnector.sql(sql_statement)

        # Assertions
        mock_connect.assert_called_once()
        mock_cnx.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(sql_statement)
        mock_cursor.fetchall.assert_called_once()
        mock_cnx.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_cnx.close.assert_called_once()
        self.assertEqual(result, [('row1',), ('row2',)])


if __name__ == '__main__':
    unittest.main()