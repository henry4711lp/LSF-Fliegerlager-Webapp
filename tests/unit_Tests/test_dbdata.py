import unittest
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestDBData(unittest.TestCase):

    def test_get_gprice_by_id(self):
        with patch('getConfig.get_config', return_value='test'):
            import src.dbdata as dbdata
        with patch('src.dbdata.dbconnector.sql') as mock_sql:
            mock_sql.return_value = [(1.5,)]
            result = dbdata.get_gprice_by_id('1')
            self.assertEqual(result, '1,50 \u20ac')
            mock_sql.assert_called_once_with('SELECT GPREIS FROM GETR WHERE GID = 1')

    def test_get_sum_of_drink_by_id_and_gid(self):
        with patch('getConfig.get_config', return_value='test'):
            import src.dbdata as dbdata
        with patch('src.dbdata.dbconnector.sql') as mock_sql:
            mock_sql.return_value = [(2.5,)]
            result = dbdata.get_sum_of_drink_by_id_and_gid('1', '2')
            self.assertEqual(result, '2,50 \u20ac')
            mock_sql.assert_called_once_with('SELECT GPREIS*CT FROM PERSGET NATURAL JOIN GETR WHERE ID = 1 AND GID = 2')


if __name__ == '__main__':
    unittest.main()
