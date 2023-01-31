"""
User authorization
"""

import jwt
from fastapi import Request
from consys.errors import ErrorWrong

from models.user import User
from models.token import Token
from models.socket import Socket
from lib import cfg


# pylint: disable=too-many-branches
def get_user(token_id=None, socket_id=None, token_jwt=None, user_id=None):
    """ Get user object by token / socket / id """

    if token_jwt is not None:
        try:
            token = jwt.decode(token_jwt, cfg('jwt'), algorithms='HS256')
        except Exception:  # pylint: disable=broad-except
            pass
        else:
            return User.get(token['user']), token['token']

    elif token_id is not None:
        try:
            token = Token.get(token_id, fields={'user'})
        except ErrorWrong:
            token = Token(id=token_id)
            token.save()
        else:
            if token.user:
                return User.get(token.user), token_id

    elif socket_id is not None:
        try:
            socket = Socket.get(socket_id, fields={'user'})
        except ErrorWrong:
            pass
        else:
            token_id = socket.token
            if socket.user:
                return User.get(socket.user), token_id

    elif user_id:
        try:
            user = User.get(user_id)
        except ErrorWrong:
            pass
        else:
            return user, None

    return User(), token_id

def sign(request: Request):
    """ Get user """
    user, _ = get_user(user_id=request.state.user)
    return user
