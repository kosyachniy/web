"""
The getting method of the user object of the API
"""

from typing import Union

from ...funcs import BaseType, validate, online_back
from ...models.user import User
from ...errors import ErrorAccess


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    fields: list[str] = None

@validate(Type)
async def handle(this, request):
    """ Get """

    # TODO: cursor

    # No access
    if this.user.status < 2:
        raise ErrorAccess('get')

    # TODO: Get myself
    # if not request.id and this.user.id:
    #     request.id = this.user.id

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

    process_self = request.id == this.user.id
    # process_moderator = this.user.status'>= 5
    process_admin = this.user.status >= 7

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

    if request.fields:
        fields = fields & set(request.fields)

    # Get
    users = User.get(
        ids=request.id,
        count=request.count,
        offset=request.offset,
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
