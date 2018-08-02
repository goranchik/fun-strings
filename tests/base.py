import unittest

from werkzeug.security import generate_password_hash

from api import app
from data.storages import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.TEST_USERNAME = 'test_user'
        self.TEST_PASSWORD = 'test_password'
        self.TEST_TOKEN = 'test_token'
        self.TEST_USER = User(self.TEST_USERNAME,
                              generate_password_hash(self.TEST_PASSWORD),
                              generate_password_hash(self.TEST_TOKEN))
        app.config['USERS'][self.TEST_USERNAME] = self.TEST_USER
        self.TEST_AUTH = {'x-access-user': self.TEST_USERNAME, 'x-access-token': self.TEST_TOKEN}
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
