import unittest
from unittest.mock import patch

from flask import url_for
from werkzeug.exceptions import BadRequest

from api import app
from settings import MESSAGES, WRONG_API_KEY
from .base import BaseTestCase


class RandomWordTestCase(BaseTestCase):

    def setUp(self):
        super(RandomWordTestCase, self).setUp()
        self.TEST_VALID_API_KEY = 'test_valid_api_key'
        self.TEST_INVALID_API_KEY = 'test_invalid_api_key'
        self.TEST_RANDOM_WORD = 'test_random_word'
        app.config['WORDS'] = ['apple', 'block']

    def _mock_get_random_word_resp(self, api_key):
        if self.TEST_INVALID_API_KEY == api_key:
            return WRONG_API_KEY
        else:
            return [self.TEST_RANDOM_WORD]

    def test_random_word_unauth(self):
        with app.test_request_context():
            resp = self.app.get(url_for('random_word'))

        self.assertEqual(resp.status_code, 401)

    def test_random_word_post(self):
        with app.test_request_context():
            resp = self.app.post(url_for('random_word'))

        self.assertEqual(resp.status_code, 405)

    def test_random_word_ok(self):
        with app.test_request_context():
            with patch('external._get_random_word_resp', side_effect=self._mock_get_random_word_resp), \
                 patch('external._get_random_api_key', return_value=self.TEST_VALID_API_KEY):
                resp = self.app.get(url_for('random_word'), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['word'], self.TEST_RANDOM_WORD)

    def test_random_word_invalid_valid_key(self):
        with app.test_request_context():
            with patch('external._get_random_word_resp',
                       side_effect=self._mock_get_random_word_resp) as random_mock, \
                    patch('external._get_random_api_key',
                          side_effect=[self.TEST_INVALID_API_KEY, self.TEST_VALID_API_KEY]):
                resp = self.app.get(url_for('random_word'), headers=self.TEST_AUTH)
                random_mock.assert_called_with(self.TEST_VALID_API_KEY)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['word'], self.TEST_RANDOM_WORD)

    def test_random_word_alternate_ok(self):
        with app.test_request_context():
            with patch('external._get_random_word_resp', side_effect=BadRequest('Test')), \
                 patch('external._get_random_api_key', return_value=self.TEST_VALID_API_KEY):
                resp = self.app.get(url_for('random_word'), headers=self.TEST_AUTH)
                resp2 = self.app.get(url_for('random_word'), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp2.status_code, 200)

        self.assertIn(resp.json['word'], app.config['WORDS'])
        self.assertIn(resp2.json['word'], app.config['WORDS'])

    def test_random_word_alternate_empty_dict(self):
        app.config['WORDS'] = []
        with app.test_request_context():
            with patch('external._get_random_word_resp', side_effect=BadRequest('Test')), \
                 patch('external._get_random_api_key', return_value=self.TEST_VALID_API_KEY), \
                 patch('api._init_words', side_effect=None):
                resp = self.app.get(url_for('random_word'), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(MESSAGES['ERR_DICT'].encode(), resp.data)


if __name__ == "__main__":
    unittest.main()
