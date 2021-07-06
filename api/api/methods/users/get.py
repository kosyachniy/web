"""
The getting method of the user object of the API
"""

from ...funcs import check_params, online_back
from ...models.user import User


async def handle(this, **x):
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

    # Processing
    if isinstance(users, list):
        for i, user in enumerate(users):
            user = user.json(default=False, fields=fields)
            user['online'] = online_back(user['id'])
            users[i] = user
    else:
        users = users.json(default=False, fields=fields)
        users['online'] = online_back(users['id'])

    # Response
    return {
        'users': users,
    }
