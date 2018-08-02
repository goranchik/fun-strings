import random
import signal
import string
import sys
import uuid

from flask import Flask, jsonify, request, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest

import external as ext
from data.storages import User, users, words, wiki_hits, load_data, dump_data, load_words, dump_words
from decorators import token_required
from settings import ERRORS, MESSAGES

app = Flask(__name__)

app.config['WORDS'] = words
app.config['USERS'] = users
app.config['WIKI_HITS'] = wiki_hits


@app.route('/')
def index():
    return jsonify([{"endpoint": r.rule, "methods": list(r.methods)} for r in app.url_map.iter_rules()])


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        abort(400, MESSAGES['NO_CREDENTIALS'])

    username = data.get('username')

    if username in app.config['USERS'].keys():
        abort(400, MESSAGES['USER_EXISTS'].format(username))
    else:
        user = User(username, generate_password_hash(data.get('password')), None)
        app.config['USERS'][username] = user

    return jsonify({'message': MESSAGES['SIGNED_UP'].format(username)}), 201


@app.route('/api/login', methods=['GET'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        abort(401, MESSAGES['AUTH_FAIL_CREDENTIALS'])
    elif auth.username not in app.config['USERS'].keys():
        abort(401, MESSAGES['AUTH_FAIL_NO_USER'].format(auth.username, url_for('signup')))

    user = app.config['USERS'].get(auth.username)

    if not check_password_hash(user.password, auth.password):
        abort(401, MESSAGES['AUTH_FAIL_WRONG_PASS'])

    token = _get_token()
    hashed_token = generate_password_hash(token)

    user_with_token = User(user.username, user.password, hashed_token)

    app.config['USERS'][user.username] = user_with_token

    return jsonify({'token': token})


@app.route('/api/randomword', methods=['GET'])
@token_required
def random_word():
    try:
        return jsonify({'word': ext.get_random_word()}), 200
    except BadRequest:
        return _alternate_random_word()


@app.route('/api/wiki/<word>', methods=['GET'])
@token_required
def wiki_content(word):
    app.config['WIKI_HITS'][word] += 1

    wiki = ext.get_wiki(word)

    if wiki.get('missing'):
        abort(404, MESSAGES['ERR_NO_ARTICLE'].format(word))
    else:
        return jsonify({'content': wiki}), 200


@app.route('/api/wiki', methods=['GET'])
@token_required
def wiki_top():
    top = request.args.get('top', 1) or 1

    try:
        n = int(top)
    except ValueError:
        abort(400, MESSAGES['ERR_INVALID_TOP'])

    return jsonify({'top': _get_wiki_top(n)}), 200


@app.route('/api/joke', methods=['GET'])
@token_required
def joke():
    args = request.args
    names = {k: args[k] for k in args.keys()}

    j = ext.get_joke(names)

    if j['type'] == 'success':
        return jsonify({'joke': j['value']['joke']}), 200
    else:
        abort(400, MESSAGES['ERR_JOKE'])


def _error_handler(err):
    return jsonify({'error': str(err)}), err.code


def _reg_error_handlers(codes: list):
    for code in codes:
        app.register_error_handler(code, _error_handler)


def _alternate_random_word():
    load_words()

    if not app.config['WORDS']:
        _init_words()

    if not app.config['WORDS']:
        abort(400, MESSAGES['ERR_DICT'])

    return jsonify({'word': random.choice(app.config['WORDS'])})


def _init_words():
    for l in string.ascii_lowercase:
        items = list(ext.get_words(l))
        app.config['WORDS'].extend(list(item['word'] for item in items))

    dump_words()


def _get_wiki_top(n: int):
    sorted_wiki_hits = sorted(app.config['WIKI_HITS'].items(), key=lambda item: item[1], reverse=True)
    return list(w for w, c in sorted_wiki_hits[:n])


def _get_token():
    return str(uuid.uuid4())


# dump data before exit to save state between stop/next start
def _exit(*args):
    dump_data()
    sys.exit(0)


signal.signal(signal.SIGINT, _exit)
signal.signal(signal.SIGTERM, _exit)


if __name__ == '__main__':
    load_data()
    _reg_error_handlers(ERRORS)
    app.run(debug=True)
