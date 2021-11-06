"""
Filename: login.py

Purpose:
Contains the login endpoints and functions for the application.

Authors: Tammas Hicks, Jordan Smith
Group: //Todo
Last modified: 10/27/21
"""
import flask
import jwt
import json
from datetime import datetime, timedelta

###
#   Globals
###
login_page = flask.Blueprint('login_page', __name__)

JWT_SECRET = 'test_secret'      # Will be randomized when actually being used
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = (20 * 60)

# Sample "users" for testing purposes
VALID_USERS = [
    {
        "id": "1",
        "username": "testuser",
        "password": "password1"
    },
    {
        "id": "2",
        "username": "another_user",
        "password": "123"
    }
]

###
#   Helper functions
###
def generate_token(user):
    payload = {
        'user_id': user['id'],
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)



###
#   Route endpoints
###
@login_page.route('/create_account', methods=["POST"])
def create_account():
    request_data = json.loads(flask.request.data)

    for USER in VALID_USERS:
        if (request_data['username'] == USER['username']):
            return {'message': 'user exists already'}, 409

    VALID_USERS.append({"id": str(len(VALID_USERS)), "username": request_data['username'], "password": request_data['password']})

    return {'message': 'success'}, 201

@login_page.route('/login', methods=["POST"])
def login():
    # Get the data from the request
    request_data = flask.request.data

    # Convert the data to a dictionary
    user_data = json.loads(request_data.decode('utf-8').replace("'", '"'))

    current_user = None

    # Get the user from the list of valids
    for USER in VALID_USERS:
        if (user_data['username'] == USER['username'] and
           user_data['password'] == USER['password']):
            current_user = USER
    
    if current_user is None:
        return flask.Response({'message': 'Wrong credentials!'}, status=400)
    
    token = generate_token(current_user)
    return  {'token': token}, 200

@login_page.route('/check_token')
def validate_token():
    # Get the token from the header
    jwt_token = flask.request.headers.get("Authorization")

    # Make sure the token exists
    if jwt_token is not None:
        # Try to decode, if it works, return the payload
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET, JWT_ALGORITHM)
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {"message": "Invalid token"}, 400

        return payload, 200
    else:
        return {"message": "Token could not be read"}, 400
