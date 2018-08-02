ERRORS = [400, 401, 404, 405, 500]

# external urls
URLS = {
    'WIKI_URL': 'https://en.wikipedia.org/w/api.php?'
                'action=query&'
                'titles={}&'
                'prop=revisions&'
                'rvprop=content&'
                'format=json&'
                'formatversion=2',
    'DATAMUSE_URL': 'https://api.datamuse.com/sug?s={}&max={}',
    'JOKE_URL': 'http://api.icndb.com/jokes/random',
    'RANDOM_WORD': 'https://random-word-api.herokuapp.com/word?key={}&number=1',
    'RANDOM_WORD_KEY': 'https://random-word-api.herokuapp.com/key'
}

MESSAGES = {
    'NO_CREDENTIALS': 'Please provide username/password. They both are required for signup',
    'USER_EXISTS': 'User {} already exists. Please try another one',
    'SIGNED_UP': 'User {} successfully signed up!',
    'AUTH_FAIL_CREDENTIALS': 'Authorization failed. Login/password required',
    'AUTH_FAIL_NO_USER': 'Authorization failed. User {} does not exist. Please signup by link {}',
    'AUTH_FAIL_WRONG_PASS': 'Authorization failed. Wrong password',
    'AUTH_USER_REQUIRED': 'Authentication failed. Username is required (header x-access-user)!',
    'AUTH_WRONG_USER': 'Authentication failed. Wrong username!',
    'AUTH_TOKEN_EXPIRED': 'Authentication failed. Token is expired! Please login again',
    'AUTH_TOKEN_REQUIRED': 'Authentication failed. Token is required (header x-access-token)!',
    'AUTH_TOKEN_INVALID': 'Authentication failed. Token is invalid!',
    'ERR_JOKE': 'Error happened when trying to get joke (:',
    'ERR_DICT': 'Dictionary is empty',
    'ERR_NO_ARTICLE': 'There is no article for word: {}. Please check spelling',
    'ERR_INVALID_TOP': 'Invalid type for \'top\' parameter. Expected type: int',
    'ERR_HTTP': 'Http error: {}',
    'ERR_TIMEOUT': 'Timeout error: {}',
    'ERR_CONNECT': 'Connection error: {}',
    'ERR_REQUEST': 'Request error: {}',
    'ERR_INTERNAL': 'Application error. Please contact support'
}

JSON_MIME_TYPE = 'application/json'
WORDS_LIMIT = 500
TIME_OUT = 5
DEFAULT_JOKE_NAMES = {'firstName': 'Chuck', 'lastName': 'Norris'}
WRONG_API_KEY = 'wrong API key'
