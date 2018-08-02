import unittest
from base64 import b64encode
from unittest.mock import patch

from flask import url_for

from api import app
from settings import MESSAGES
from .base import BaseTestCase


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super(LoginTestCase, self).setUp()

    def _get_auth_header(self):
        _auth = self.TEST_USERNAME + ':' + self.TEST_PASSWORD
        _b64_auth = b64encode(_auth.encode())
        _basic_auth_str = 'Basic {}'.format(_b64_auth.decode())
        return {'Authorization': _basic_auth_str}

    def test_login_post(self):
        with app.test_request_context():
            resp = self.app.post(url_for('joke'))

        self.assertEqual(resp.status_code, 405)

    def test_login_blank_auth(self):
        self.TEST_USERNAME = ''
        self.TEST_PASSWORD = ''
        with app.test_request_context():
            resp = self.app.get(url_for('login'),
                                headers=self._get_auth_header())

        self.assertEqual(resp.status_code, 401)
        self.assertIn(MESSAGES['AUTH_FAIL_CREDENTIALS'].encode(), resp.data)

    def test_login_blank_username(self):
        self.TEST_USERNAME = ''
        with app.test_request_context():
            resp = self.app.get(url_for('login'),
                                headers=self._get_auth_header())

        self.assertEqual(resp.status_code, 401)
        self.assertIn(MESSAGES['AUTH_FAIL_CREDENTIALS'].encode(), resp.data)

    def test_login_blank_password(self):
        self.TEST_PASSWORD = ''
        with app.test_request_context():
            resp = self.app.get(url_for('login'),
                                headers=self._get_auth_header())

        self.assertEqual(resp.status_code, 401)
        self.assertIn(MESSAGES['AUTH_FAIL_CREDENTIALS'].encode(), resp.data)

    def test_login_wrong_password(self):
        self.TEST_PASSWORD = 'wrong'
        with app.test_request_context():
            resp = self.app.get(url_for('login'),
                                headers=self._get_auth_header())

        self.assertEqual(resp.status_code, 401)
        self.assertIn(MESSAGES['AUTH_FAIL_WRONG_PASS'].encode(), resp.data)

    def test_login_no_user(self):
        app.config['USERS'] = {}
        with app.test_request_context():
            with patch('api._get_token', return_value=self.TEST_TOKEN):
                resp = self.app.get(url_for('login'),
                                    headers=self._get_auth_header())

        self.assertEqual(resp.status_code, 401)
        self.assertIn(MESSAGES['AUTH_FAIL_NO_USER'].format(self.TEST_USERNAME, '').encode(), resp.data)

    def test_login_success(self):
        with app.test_request_context():
            with patch('api._get_token', return_value=self.TEST_TOKEN):
                resp = self.app.get(url_for('login'),
                                    headers=self._get_auth_header())

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.TEST_TOKEN, resp.json['token'])


if __name__ == '__main__':
    unittest.main()
