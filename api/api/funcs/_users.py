"""
Users functionality for the API
"""

from .mongodb import db
from ..models.user import User
from ..models.token import Token


def get_user(token_id):
    """ Get user object by token """

    if token_id is not None:
        token = Token.get(ids=token_id)

        if token.user:
            return User.get(ids=token.user)
    
    return User()

def get_status(user):
    """ Get available status for the user """

    if user['status'] >= 6:
        return 0

    if user['status'] >= 5:
        return 1

    if user['status'] >= 3:
        return 3

    return 3 # !

def get_status_condition(user):
    """ Get conditions for database by user """

    if user['id']:
        return {
            '$or': [{
                'status': {'$gte': get_status(user)},
            }, {
                'user': user['id'],
            }]
        }

    return {
        'status': {'$gte': get_status(user)},
    }

def get_id(sid):
    """ Get user ID by sid """

    db_filter = {
        '_id': False,
        'id': True,
    }

    user = db['sockets'].find_one({'sid': sid}, db_filter)

    if not user:
        raise Exception('sid not found')

    # ?
    if not isinstance(user['id'], int) or not user['id']:
        return 0

    return user['id']

def get_sids(user):
    """ Get all sids of user by ID """

    db_filter = {
        '_id': False,
        'sid': True,
    }

    user_sessions = db['sockets'].find({'id': user}, db_filter)

    return [i['sid'] for i in user_sessions]
