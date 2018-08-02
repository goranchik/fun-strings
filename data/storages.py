import json
import os
from collections import defaultdict, namedtuple

# the following data structures are used across the app (sort of singleton)
users = {}
words = []
wiki_hits = defaultdict(int)

FILES = {
    'USERS': 'users.json',
    'WORDS': 'words.json',
    'WIKI_HITS': 'wiki_hits.json'
}

User = namedtuple('User', ['username', 'password', 'token'])


def load_data():
    _load_users()
    _load_wiki_hits()


def load_words():
    file_path = _get_path(FILES['WORDS'])
    if os.path.exists(file_path):
        with open(file_path) as words_file:
            words.extend(json.load(words_file))


def dump_data():
    _dump('USERS', users)
    _dump('WIKI_HITS', wiki_hits)


def dump_words():
    _dump('WORDS', words)


def _get_path(f: str):
    return os.path.dirname(__file__) + '/' + f


def _load_users():
    file_path = _get_path(FILES['USERS'])
    if os.path.exists(file_path):
        with open(file_path) as users_file:
            for k, v in json.load(users_file).items():
                users[k] = User(v[0], v[1], v[2])


def _load_wiki_hits():
    file_path = _get_path(FILES['WIKI_HITS'])
    if os.path.exists(file_path):
        with open(file_path) as wiki_hits_file:
            for k, v in json.load(wiki_hits_file).items():
                wiki_hits[k] = v


def _dump(storage_name: str, storage):
    if storage:
        file_path = _get_path(FILES[storage_name])
        with open(file_path, 'w') as f:
            json.dump(storage, f)
