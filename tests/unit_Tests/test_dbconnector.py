import unittest
from unittest.mock import patch, MagicMock
import src.dbconnector as dbconnector
from src import getConfig


class TestDBConnector(unittest.TestCase):

    @patch('src.dbconnector.mysql.connector.connect')
    def test_sql(self, mock_connect):
        # Mock the database connection and cursor
        mock_cnx = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_cnx
        mock_cnx.is_connected.return_value = True
        mock_cnx.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]

        # SQL statement to be tested
        sql_statement = "SELECT * FROM test_table"

        # Call the function
        result = dbconnector.sql(sql_statement)

        # Assertions
        mock_connect.assert_called_once_with(user=getConfig.get_config("db_user"), password=getConfig.get_config("db_password"),
                                  host=getConfig.get_config("db_host"), database=getConfig.get_config("db_name"),
                                  port=getConfig.get_config("db_port"),
                                  ssl_disabled=getConfig.get_config("db_ssl_disabled"))
        mock_cnx.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(sql_statement)
        mock_cursor.fetchall.assert_called_once()
        mock_cnx.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_cnx.close.assert_called_once()
        self.assertEqual(result, [('row1',), ('row2',)])


if __name__ == '__main__':
    unittest.main()