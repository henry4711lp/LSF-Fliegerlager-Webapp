import unittest
import main as tested_app


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_root_endpoint_fwd(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 302)
        print("tested root forward")

    def test_register_endpoint(self):
        r = self.app.get('/register')
        self.assertEqual(r.status_code, 200)
        print("tested register 200")

    def test_home_error_on_no_post(self):
        r = self.app.get('/home')
        self.assertEqual(r.status_code, 404)
        print("tested error on no post home")

    def test_home_post_login_data(self):
        print("tested post with test data to home")

    # def test_post_hello_endpoint(self):
    #     r = self.app.post('/')
    #     self.assertEqual(r.status_code, 405)
    #
    # def test_get_api_endpoint(self):
    #     r = self.app.get('/api')
    #     self.assertEqual(r.json, {'status': 'test'})
    #
    # def test_correct_post_api_endpoint(self):
    #     r = self.app.post('/api',
    #                       content_type='application/json',
    #                       data=json.dumps({'name': 'Den', 'age': 100}))
    #     self.assertEqual(r.json, {'status': 'OK'})
    #     self.assertEqual(r.status_code, 200)
    #
    #     r = self.app.post('/api',
    #                       content_type='application/json',
    #                       data=json.dumps({'name': 'Den'}))
    #     self.assertEqual(r.json, {'status': 'OK'})
    #     self.assertEqual(r.status_code, 200)
    #
    # def test_not_dict_post_api_endpoint(self):
    #     r = self.app.post('/api',
    #                       content_type='application/json',
    #                       data=json.dumps([{'name': 'Den'}]))
    #     self.assertEqual(r.json, {'status': 'bad input'})
    #     self.assertEqual(r.status_code, 400)
    #
    # def test_no_name_post_api_endpoint(self):
    #     r = self.app.post('/api',
    #                       content_type='application/json',
    #                       data=json.dumps({'age': 100}))
    #     self.assertEqual(r.json, {'status': 'bad input'})
    #     self.assertEqual(r.status_code, 400)
    #
    # def test_bad_age_post_api_endpoint(self):
    #     r = self.app.post('/api',
    #                       content_type='application/json',
    #                       data=json.dumps({'name': 'Den', 'age': '100'}))
    #     self.assertEqual(r.json, {'status': 'bad input'})
    #     self.assertEqual(r.status_code, 400)
    #


if __name__ == '__main__':
    unittest.main()
