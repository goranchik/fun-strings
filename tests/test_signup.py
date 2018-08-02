import unittest

from flask import url_for, json

from api import app
from settings import MESSAGES, JSON_MIME_TYPE
from .base import BaseTestCase


class SignUpTestCase(BaseTestCase):

    def setUp(self):
        super(SignUpTestCase, self).setUp()

    def test_sign_up_blank(self):
        with app.test_request_context():
            resp = self.app.post(url_for('signup'), data=json.dumps({}))

        self.assertEqual(resp.status_code, 400)
        self.assertIn(MESSAGES['NO_CREDENTIALS'].encode(), resp.data)

    def test_sign_up_blank_username(self):
        with app.test_request_context():
            resp = self.app.post(url_for('signup'),
                                 data=json.dumps({'password': self.TEST_PASSWORD}),
                                 content_type=JSON_MIME_TYPE)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(MESSAGES['NO_CREDENTIALS'].encode(), resp.data)

    def test_sign_up_blank_password(self):
        with app.test_request_context():
            resp = self.app.post(url_for('signup'),
                                 data=json.dumps({'username': self.TEST_USERNAME}),
                                 content_type=JSON_MIME_TYPE)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(MESSAGES['NO_CREDENTIALS'].encode(), resp.data)

    def test_sign_up_user_exists(self):
        with app.test_request_context():
            resp = self.app.post(url_for('signup'),
                                 data=json.dumps({'username': self.TEST_USERNAME,
                                                  'password': self.TEST_PASSWORD}),
                                 content_type=JSON_MIME_TYPE)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(MESSAGES['USER_EXISTS'].format(self.TEST_USERNAME).encode(), resp.data)

    def test_sign_up_success(self):
        new_username = 'new_test_user'
        with app.test_request_context():
            resp = self.app.post(url_for('signup'),
                                 data=json.dumps({'username': new_username,
                                                  'password': self.TEST_PASSWORD}),
                                 content_type=JSON_MIME_TYPE)

        self.assertEqual(resp.status_code, 201)
        self.assertIn(MESSAGES['SIGNED_UP'].format(new_username).encode(), resp.data)


if __name__ == '__main__':
    unittest.main()
