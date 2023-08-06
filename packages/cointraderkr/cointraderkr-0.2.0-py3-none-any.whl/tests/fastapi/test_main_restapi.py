from unittest import TestCase
from fastapi.testclient import TestClient

from main import app


class TestMainRestAPI(TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        pass

    def test_1_client_works(self):
        self.assertIsInstance(self.client, TestClient)

    def test_2_can_get_logs(self):
        response = self.client.get('/log')
        response_json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('length', response_json.keys())

    def test_3_can_save_log(self):
        log = {
            'source': 'test',
            'ip_address': '127.0.0.1',
            'log_level': 'info',
            'message': 'test log message'
        }

        prev_log_response = self.client.get('/log')
        response = self.client.post('/log', json=log)
        post_log_response = self.client.get('/log')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(prev_log_response.json()['length'] + 1,
                         post_log_response.json()['length'])