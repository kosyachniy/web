"""
User authorization
"""

from fastapi import Body
from pydantic import BaseModel
from consys.errors import ErrorWrong

from models.user import User
from models.token import Token
from models.socket import Socket


def get_user(token_id, socket_id=None, jwt=None):
    """ Get user object by token """

    if token_id is not None:
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
                return User.get(ids=socket.user), token_id

    elif jwt is not None:
        users = User.get(social={'$elemMatch': {
            'id': jwt['network'],
            'user': jwt['user'],
        }})

        if users:
            return users[0], token_id

    return User(), token_id


class Type(BaseModel):
    token: str

def auth(data: Type = Body(...)):
    """ User authorization """
    user, _ = get_user(data.token)
    return user

def get_token(data: Type = Body(...)):
    """ Get token """
    _, token = get_user(data.token)
    return token
