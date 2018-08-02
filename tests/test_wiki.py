import unittest
from collections import defaultdict
from unittest.mock import patch

from flask import url_for

from api import app
from settings import MESSAGES
from .base import BaseTestCase


class WikiTestCase(BaseTestCase):

    def setUp(self):
        super(WikiTestCase, self).setUp()
        self.TEST_WORD = 'apple'
        self.TEST_WORD1 = 'cherry'
        self.TEST_WORD2 = 'blueberry'
        self.TEST_WORD3 = 'blackberry'
        self.BAD_WORD = 'test_bad_word'
        self.TEST_ARTICLE = 'Test article about {}'

    def _mock_wiki(self, word):
        if self.BAD_WORD == word:
            return {'missing': True}
        else:
            return {'article': self.TEST_ARTICLE.format(word)}

    def test_wiki_unauth(self):
        with app.test_request_context():
            resp_content = self.app.get(url_for('wiki_content', word=self.TEST_WORD))
            resp_top = self.app.get(url_for('wiki_top'))

        self.assertEqual(resp_content.status_code, 401)
        self.assertEqual(resp_top.status_code, 401)

    def test_wiki_post(self):
        with app.test_request_context():
            resp_content = self.app.post(url_for('wiki_content', word=self.TEST_WORD))
            resp_top = self.app.post(url_for('wiki_top'))

        self.assertEqual(resp_content.status_code, 405)
        self.assertEqual(resp_top.status_code, 405)

    def test_wiki_bad_word(self):
        with app.test_request_context():
            with patch('external.get_wiki', self._mock_wiki):
                resp = self.app.get(url_for('wiki_content', word=self.BAD_WORD), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 404)
        self.assertIn(MESSAGES['ERR_NO_ARTICLE'].format(self.BAD_WORD).encode(), resp.data)

    def test_wiki_good_word(self):
        app.config['WIKI_HITS'] = defaultdict(int)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD], 0)
        with app.test_request_context():
            with patch('external.get_wiki', self._mock_wiki):
                self.app.get(url_for('wiki_content', word=self.TEST_WORD), headers=self.TEST_AUTH)
                resp = self.app.get(url_for('wiki_content', word=self.TEST_WORD), headers=self.TEST_AUTH)

        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD], 2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({'article': self.TEST_ARTICLE.format(self.TEST_WORD)}, resp.json['content'])

    def test_wiki_without_top(self):
        app.config['WIKI_HITS'] = defaultdict(int)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD] +
                         app.config['WIKI_HITS'][self.TEST_WORD1],
                         0)
        with app.test_request_context():
            with patch('external.get_wiki', self._mock_wiki):
                for i in range(10):
                    self.app.get(url_for('wiki_content', word=self.TEST_WORD), headers=self.TEST_AUTH)

                for i in range(5):
                    self.app.get(url_for('wiki_content', word=self.TEST_WORD1), headers=self.TEST_AUTH)

                resp = self.app.get(url_for('wiki_top'), headers=self.TEST_AUTH)

        self.assertNotEqual(app.config['WIKI_HITS'][self.TEST_WORD] +
                            app.config['WIKI_HITS'][self.TEST_WORD1],
                            0)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD], 10)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD1], 5)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(1, len(resp.json['top']))
        self.assertEqual(self.TEST_WORD, resp.json['top'][0])

    def test_wiki_with_top3(self):
        app.config['WIKI_HITS'] = defaultdict(int)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD] +
                         app.config['WIKI_HITS'][self.TEST_WORD1] +
                         app.config['WIKI_HITS'][self.TEST_WORD2] +
                         app.config['WIKI_HITS'][self.TEST_WORD3],
                         0)
        with app.test_request_context():
            with patch('external.get_wiki', self._mock_wiki):
                for i in range(2):
                    self.app.get(url_for('wiki_content', word=self.TEST_WORD), headers=self.TEST_AUTH)

                for i in range(10):
                    self.app.get(url_for('wiki_content', word=self.TEST_WORD1), headers=self.TEST_AUTH)

                for i in range(15):
                    self.app.get(url_for('wiki_content', word=self.TEST_WORD2), headers=self.TEST_AUTH)

                for i in range(5):
                    self.app.get(url_for('wiki_content', word=self.TEST_WORD3), headers=self.TEST_AUTH)

                resp = self.app.get(url_for('wiki_top', top=3), headers=self.TEST_AUTH)

        self.assertNotEqual(app.config['WIKI_HITS'][self.TEST_WORD] +
                            app.config['WIKI_HITS'][self.TEST_WORD1] +
                            app.config['WIKI_HITS'][self.TEST_WORD2] +
                            app.config['WIKI_HITS'][self.TEST_WORD3],
                            0)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD], 2)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD1], 10)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD2], 15)
        self.assertEqual(app.config['WIKI_HITS'][self.TEST_WORD3], 5)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3, len(resp.json['top']))
        self.assertEqual([self.TEST_WORD2, self.TEST_WORD1, self.TEST_WORD3], resp.json['top'])

    def test_wiki_with_invalid_top(self):
        with app.test_request_context():
            resp = self.app.get(url_for('wiki_top', top='test'), headers=self.TEST_AUTH)

        self.assertEqual(resp.status_code, 400)
        self.assertIn(MESSAGES['ERR_INVALID_TOP'].encode(), resp.data)


if __name__ == '__main__':
    unittest.main()
