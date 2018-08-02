import requests

from decorators import resp_handler
from settings import URLS, WORDS_LIMIT, TIME_OUT, DEFAULT_JOKE_NAMES, WRONG_API_KEY

# cache for requests.sessions
sessions = {}

# cached (global) api key for external random service (to reuse between diff requests)
random_api_key = None


def get_random_word():
    global random_api_key

    if not random_api_key:
        random_api_key = _get_random_api_key()

    resp = _get_random_word_resp(random_api_key)

    if resp == WRONG_API_KEY:
        random_api_key = _get_random_api_key()
        resp = _get_random_word_resp(random_api_key)

    return resp[0]


def get_wiki(word: str):
    url_type = 'WIKI_URL'
    return _req_get(url_type, URLS[url_type].format(word)).json()['query']['pages'][0]


def get_joke(names):
    url_type = 'JOKE_URL'

    if not any(names.keys()):
        names = DEFAULT_JOKE_NAMES

    return _req_get(url_type, URLS[url_type], params=names).json()


#  alternate external service for random words (pseudo random, WORDS_LIMIT words for each l asci symbol)
def get_words(l: str):
    url_type = 'DATAMUSE_URL'
    return _req_get(url_type, URLS[url_type].format(l, WORDS_LIMIT)).json()


def _get_random_api_key():
    return _req_get('RANDOM_WORD', URLS['RANDOM_WORD_KEY']).content.decode()


def _get_random_word_resp(api_key: str):
    url_type = 'RANDOM_WORD'
    return _req_get(url_type, URLS[url_type].format(api_key)).json()


@resp_handler
def _req_get(url_type: str, url: str, **kwargs):

    if url_type not in sessions.keys():
        sessions[url_type] = requests.Session()

    return sessions[url_type].get(url, timeout=TIME_OUT, **kwargs)
