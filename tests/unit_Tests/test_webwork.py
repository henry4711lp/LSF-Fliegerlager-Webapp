import unittest
from unittest.mock import patch, MagicMock, ANY
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestWebwork(unittest.TestCase):

    def test_signup_in_new_user(self):
        request = MagicMock()
        request.form = {'vname': 'John', 'nname': 'Doe'}
        response_mock = MagicMock()
        with patch('getConfig.get_config', return_value='test'):
            import src.webwork as webwork
            with (
                patch('src.webwork.dbdata.get_id_by_name', side_effect=[[], [[1]]]) as get_id_mock,
                patch('src.webwork.dbdata.set_user_id_by_name') as set_user_mock,
                patch('src.webwork.render_template', return_value='html') as render_mock,
                patch('src.webwork.make_response', return_value=response_mock) as make_resp_mock
            ):
                result = webwork.signup_in(request)

        set_user_mock.assert_called_once_with('John', 'Doe')
        self.assertEqual(get_id_mock.call_count, 2)
        render_mock.assert_called_once_with('home.html', ID=1, date=ANY, display_name='John', display_ID='1')
        make_resp_mock.assert_called_once_with('html')
        response_mock.set_cookie.assert_called_once_with('UserID', '1', max_age=320)
        self.assertEqual(result, response_mock)


if __name__ == '__main__':
    unittest.main()
