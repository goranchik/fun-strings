import unittest
from unittest.mock import patch

from flask import url_for

from api import app
from settings import DEFAULT_JOKE_NAMES
from .base import BaseTestCase


class JokeTestCase(BaseTestCase):

    def setUp(self):
        super(JokeTestCase, self).setUp()
        self.TEST_FIRST_NAME = 'test_first_name'
        self.TEST_LAST_NAME = 'test_last_name'
        self.TEST_JOKE = 'Test joke about {} {}'

    def _mock_joke(self, names):
        if 'firstName' not in names.keys():
            names['firstName'] = DEFAULT_JOKE_NAMES['firstName']

        if 'lastName' not in names.keys():
            names['lastName'] = DEFAULT_JOKE_NAMES['lastName']

        return {'type': 'success',
                'value': {'joke': self.TEST_JOKE.format(names['firstName'], names['lastName'])}
                }

    def test_joke_unauth(self):
        with app.test_request_context():
            resp = self.app.get(url_for('joke'))

        self.assertEqual(resp.status_code, 401)

    def test_joke_post(self):
        with app.test_request_context():
            resp = self.app.post(url_for('joke'))

        self.assertEqual(resp.status_code, 405)

    def test_joke(self):
        with app.test_request_context():
            with patch('external.get_joke', side_effect=self._mock_joke):
                resp = self.app.get(url_for('joke'), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 200)

        joke = resp.json['joke']
        self.assertIsNotNone(joke)
        self.assertIn(DEFAULT_JOKE_NAMES['firstName'], joke)
        self.assertIn(DEFAULT_JOKE_NAMES['lastName'], joke)

    def test_joke_first_name(self):
        with app.test_request_context():
            with patch('external.get_joke', side_effect=self._mock_joke):
                resp = self.app.get(url_for('joke', firstName=self.TEST_FIRST_NAME), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 200)

        joke = resp.json['joke']
        self.assertIsNotNone(joke)
        self.assertIn(self.TEST_FIRST_NAME, joke)
        self.assertNotIn(DEFAULT_JOKE_NAMES['firstName'], joke)
        self.assertIn(DEFAULT_JOKE_NAMES['lastName'], joke)

    def test_joke_last_name(self):
        with app.test_request_context():
            with patch('external.get_joke', side_effect=self._mock_joke):
                resp = self.app.get(url_for('joke', lastName=self.TEST_LAST_NAME), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 200)

        joke = resp.json['joke']
        self.assertIsNotNone(joke)
        self.assertIn(DEFAULT_JOKE_NAMES['firstName'], joke)
        self.assertIn(self.TEST_LAST_NAME, joke)
        self.assertNotIn(DEFAULT_JOKE_NAMES['lastName'], joke)

    def test_joke_first_last_name(self):
        with app.test_request_context():
            with patch('external.get_joke', side_effect=self._mock_joke):
                resp = self.app.get(url_for('joke',
                                            firstName=self.TEST_FIRST_NAME,
                                            lastName=self.TEST_LAST_NAME), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 200)

        joke = resp.json['joke']
        self.assertIsNotNone(joke)
        self.assertIn(self.TEST_FIRST_NAME, joke)
        self.assertIn(self.TEST_LAST_NAME, joke)
        self.assertNotIn(DEFAULT_JOKE_NAMES['firstName'], joke)
        self.assertNotIn(DEFAULT_JOKE_NAMES['lastName'], joke)


if __name__ == "__main__":
    unittest.main()
