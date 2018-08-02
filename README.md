Fun with Strings API
----------------

The Fun with Strings API provides a RESTful API to play with English words.
The service allows to have the following operations on strings:
  - get a random word
  - return content of Wikipedia article about given word
  - collect statistic for most popular words submitted to previous operation and return top N, where N is provided by user
  - given a first and/or a last name as parameter, return a random joke (if no name is provided, a Chuck Norris joke is returned)

For the random word service there is the alternate source in case when the main is unavailable (in that case data is pre-stored on application layer).
API service is stateful, which means data will be stored (dumped/loaded to/from files) between start/stop of application.

Only authorized users will be able to access the service.

All APIs return the _20x_ HTTP response on success and _4xx/5xx_ on errors.
Responses are represented in JSON format.

E.g., an error is returned as the following JSON object in the response body:

Fields:

- _error_: a string, description of the error.

Example:

    POST /api/signup

    400 Bad Request

    {
        "error": "400 Bad Request: Please provide username/password. They both are required for signup"
    }


A success response is returned as JSON object:

Fields:

- _message_(or _specific item_): a string, or any other object as specified by the endpoint.

Example:

    GET /api/randomword

    200 OK

    {
        "word": "apple"
    }

# Generic Errors

## Application Error

    500 Internal Server Error

    {
        "error": "Application error. Please contact support"
    }

## Http error

    500 Internal Server Error

    {
        "error": "500 Internal Server Error: Http error: details"
    }

## Timeout error

    500 Internal Server Error

    {
        "error": "500 Internal Server Error: Timeout error: details"
    }

## Connection error

    500 Internal Server Error

    {
        "error": "500 Internal Server Error: Connection error: details"
    }

## Request error

    500 Internal Server Error

    {
        "error": "500 Internal Server Error: Request error: details"
    }


# End Points

## POST /api/signup

Returns message about success or an error.

Example:

    POST /api/signup

    {
        "username" : "test",
        "password" : "test"
    }

    201 CREATED

    {
        "message": "User test successfully signed up!"
    }

Errors (example):

    400 Bad Request

    {
        "error": "400 Bad Request: Please provide username/password. They both are required for signup"
    }

    400 Bad Request

    {
        "error": "400 Bad Request: User test already exists. Please try another one"
    }


## GET /api/login

Returns a token for given user to use for the following authentication.
It requires Authorization header (Basic Auth) with username/password from signup endpoint.

Example:

    GET /api/login

    200 OK

    {
        "token": "bbf63638-9768-42de-8fda-00ebf58e1e07"
    }

Errors (example):

    401 Unauthorized

    {
        "error": "401 Unauthorized: Authorization failed. Login/password required"
    }

    401 Unauthorized

    {
        "error": "401 Unauthorized: Authorization failed. Wrong password"
    }

    401 Unauthorized

    {
        "error": "401 Unauthorized: Authorization failed. User test does not exist. Please signup by link /api/signup"
    }


## GET /api/randomword

Returns a random word.
Authentication is required (headers: x-access-user, x-access-token), where x-access-user is username used for login, and x-access-token - token which is returned from login endpoint

Example:

    GET /api/randomword

    200 OK

    {
        "word": "study"
    }


## GET /api/wiki/\<word\>

Given the word, returns a content of the English Wikipedia article (JSON format).
Authentication is required

Example:

    GET /api/wiki/python

    200 OK

    {
        "content": {...}
    }

Errors (example):

    GET /api/wiki/qqqq

    404 Not Found

    {
        "error": "404 Not Found: There is no article for word: qqqq. Please check spelling"
    }


## GET /api/wiki
## GET /api/wiki?top=\<int:N\>

Returns the top _N_ words submitted to the _/api/wiki/\<word\>_ endpoint as an array of strings.
If _top_ parameter is not provided (or provided without value) it returns top 1 word.
Authentication is required.

Example:

    GET /api/wiki

    200 OK

    {
        "top": [
            "python"
        ]
    }

    GET /api/wiki?top

    200 OK

    {
        "top": [
            "python"
        ]
    }


    GET /api/wiki?top=2

    200 OK

    {
        "top": [
            "python",
            "java"
        ]
    }

Errors (example):

    GET /api/wiki?top=t

    400 Bad Request

    {
        "error": "400 Bad Request: Invalid type for 'top' parameter. Expected type: int"
    }

## GET /api/joke
## GET /api/joke?firstName=\<firstName\>
## GET /api/joke?lastName=\<lastName\>
## GET /api/joke?firstName=\<firstName\>&lastName=\<lastName\>

Returns a joke for the given a first and/or a last name.
If either the _firstName_ or _lastName_ or both names are missing, they are replaced with the _Norris_ and _Chuck_ respectively.

Example:

    GET /api/joke

    200 OK

    {
        "joke": "Bill Gates thinks he's Chuck Norris. Chuck Norris actually laughed. Once."
    }

    GET /api/joke?firstName=Steve

    200 OK

    {
        "joke": "No one has ever spoken during review of Steve Norris' code and lived to tell about it."
    }

    GET /api/joke?lastName=Ellison

    200 OK

    {
        "joke": "Everything King Midas touches turnes to gold. Everything Chuck Ellison touches turns up dead."
    }

    GET /api/joke?firstName=Steve&lastName=Bale

    200 OK

    {
        "joke": "Steve Bale can make onions cry."
    }

Errors (example):

    GET /api/joke

    400 Bad Request

    {
        "error": "400 Bad Request: Error happened when trying to get joke (:"
    }

Environment And Dependencies
----------------------------

In order to install the extra dependencies run:

    $ pip install -r requirements.txt


Testing
-------

In order to install testing dependencies run:

    $ pip install -r test-requirements.txt


Then run:

    $ python -m unittest


Running
-------

To run the application (Debug mode: on, by default):

    $ python api.py
