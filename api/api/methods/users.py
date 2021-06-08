"""
Users object of the API
"""

from ..funcs import check_params
from ..funcs.mongodb import db
from ..models.user import User
from ..errors import ErrorWrong, ErrorAccess


async def get(this, **x):
    """ Get """

    # Checking parameters

    check_params(x, (
        ('id', False, (int, list), int),
        ('count', False, int),
        ('offset', False, int),
        ('fields', False, list, str),
    ))

    # Fields

    fields = {
        'id',
        'login',
        'name',
        'surname',
        'avatar',
        'status',
        # 'balance',
        # 'rating',
        # 'description',
        # 'online',
    }

    process_self = 'id' in x and x['id'] == this.user['id']
    # process_moderator = this.user['status'] >= 5
    process_admin = this.user['status'] >= 7

    if process_self:
        fields |= {
            'mail',
            'social',
            # 'phone',
        }

    # if process_moderator:
    #     fields |= {
    #         'transactions',
    #     }

    if process_admin:
        fields |= {
            'mail',
            'social',
            # 'phone',
        }

    # Get

    users = User.get(
        ids=x.get('id', None),
        count=x.get('count', None),
        offset=x.get('offset', None),
        fields=fields,
    )

    # # Processing

    # for i in range(len(users)):
    #     # Online
    #     users[i]['online'] = db['sockets'].find_one(
    #         {'id': users[i]['id']},
    #         {'_id': True}
    #     ) == True

    # Response

    res = {
        'users': users,
    }

    return res

async def block(this, **x):
    """ Block """

    # Checking parameters

    check_params(x, (
        ('id', True, int),
    ))

    # Get user

    users = db['users'].find_one({'id': x['id']})

    ## Wrond ID
    if not users:
        raise ErrorWrong('id')

    # No access
    if this.user['status'] < 6 or users['status'] > this.user['status']:
        raise ErrorAccess('block')

    # Change status
    users['status'] = 1

    # Save
    db['users'].save(users)
