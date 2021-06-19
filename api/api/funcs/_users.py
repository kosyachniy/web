"""
Users functionality for the API
"""

from .mongodb import db


def get_user(user_id):
    """ Get user by ID """

    if user_id:
        db_condition = {
            'id': user_id,
        }

        db_filter = {
            '_id': False,
            'id': True,
            'login': True,
            'name': True,
            'surname': True,
            'avatar': True,
        }

        user_req = db['users'].find_one(db_condition, db_filter)

        if 'avatar' in user_req:
            user_req['avatar'] = '/load/opt/' + user_req['avatar']
        else:
            user_req['avatar'] = 'user.png'

    else:
        user_req = 0

    return user_req

def get_user_by_token(token):
    """ Get user object by token """

    from ..models.user import User

    user = User()

    if not token:
        return user

    db_filter = {'user': True, '_id': False}
    token_data = db['tokens'].find_one({'token': token}, db_filter)

    if not token_data or not token_data['user']:
        return user

    try:
        user = User.get(ids=token_data['user'])
    except:
        pass

    return user

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
