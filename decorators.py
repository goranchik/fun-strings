from functools import wraps

import requests
from flask import request, abort
from werkzeug.security import check_password_hash

from data.storages import users
from settings import MESSAGES


# decorator for secured endpoints
def token_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        username, token = None, None

        if 'x-access-user' in request.headers:
            username = request.headers['x-access-user']

        if not username:
            abort(401, MESSAGES['AUTH_USER_REQUIRED'])

        if not users or username not in users.keys():
            return abort(401, MESSAGES['AUTH_WRONG_USER'])

        if not users[username].token:
            return abort(401, MESSAGES['AUTH_TOKEN_EXPIRED'])

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            abort(401, MESSAGES['AUTH_TOKEN_REQUIRED'])

        if not check_password_hash(users[username].token, token):
            return abort(401, MESSAGES['AUTH_TOKEN_INVALID'])

        return f(*args, **kwargs)

    return inner


# decorator as single point of error handling for all external APIs
def resp_handler(f):
    @wraps(f)
    def inner(*args, **kwargs):
        resp = None
        try:
            resp = f(*args, **kwargs)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            abort(500, MESSAGES['ERR_HTTP'].format(errh))
        except requests.exceptions.ConnectTimeout as errt:
            abort(500, MESSAGES['ERR_TIMEOUT'].format(errt))
        except requests.exceptions.ConnectionError as errc:
            abort(500, MESSAGES['ERR_CONNECT'].format(errc))
        except requests.exceptions.RequestException as err:
            abort(500, MESSAGES['ERR_REQUEST'].format(err))
        except Exception:
            abort(500, MESSAGES['ERR_INTERNAL'])
        return resp

    return inner
