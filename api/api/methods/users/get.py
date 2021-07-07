"""
The getting method of the user object of the API
"""

from typing import Union

from ...funcs import BaseType, validate, online_back
from ...models.user import User


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    fields: list[str] = None

@validate(Type)
async def handle(this, request):
    """ Get """

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

    process_self = request.id == this.user['id']
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
        ids=request.id,
        count=request.count,
        offset=request.offset,
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
