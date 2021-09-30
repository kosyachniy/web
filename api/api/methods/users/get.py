"""
The getting method of the user object of the API
"""

from typing import Union

from consys.errors import ErrorAccess

from ...lib import BaseType, validate, online_back
from ...models.user import User


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    fields: list[str] = None

@validate(Type)
async def handle(this, request, data):
    """ Get """

    # TODO: cursor

    # No access
    if request.user.status < 2:
        raise ErrorAccess('get')

    # TODO: Get myself
    # if not data.id and request.user.id:
    #     data.id = request.user.id

    # Fields

    fields = {
        'id',
        'login',
        'avatar',
        'name',
        'surname',
        'status',
        # 'balance',
        # 'rating',
        # 'description',
        # 'online',
    }

    process_self = data.id == request.user.id
    # process_moderator = request.user.status'>= 5
    process_admin = request.user.status >= 7

    if process_self:
        fields |= {
            'phone',
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
            'phone',
            'mail',
            'social',
            # 'phone',
        }

    if data.fields:
        fields = fields & set(data.fields)

    # Get
    users = User.get(
        ids=data.id,
        count=data.count,
        offset=data.offset,
        fields=fields,
    )

    # Processing
    # NOTE: user.json(default=True) -> login, status
    if isinstance(users, list):
        for i, user in enumerate(users):
            user = user.json(fields=fields)
            user['online'] = online_back(user['id'])
            users[i] = user
    else:
        users = users.json(fields=fields)
        users['online'] = online_back(users['id'])

    # Response
    return {
        'users': users,
    }
