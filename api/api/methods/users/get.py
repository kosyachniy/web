"""
The getting method of the user object of the API
"""

import time
from typing import Union

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.user import User
from api.models.socket import Socket


def online_back(user_id):
    """ Checking how long has been online """

    sockets = Socket.get(user=user_id, fields={})

    if sockets:
        return 0

    user = User.get(ids=user_id, fields={'online'})

    if not user.online:
        return 0

    last = user.online[-1]['stop']
    return int(time.time() - last)


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    fields: list[str] = None

@validate(Type)
async def handle(request, data):
    """ Get """

    # TODO: cursor

    # No access
    if request.user.status < 2:
        raise ErrorAccess('get')

    # TODO: Get myself
    # if not data.id and request.user.id:
    #     data.id = request.user.id

    # Fields
    # TODO: right to roles

    fields = {
        'id',
        'login',
        'avatar',
        'name',
        'surname',
        'status',
        # 'balance',
        # 'rating',
        'description',
        # 'channels',
        # 'global_channel',
        # 'discount',
    }

    process_self = data.id == request.user.id
    # process_moderator = request.user.status'>= 5
    process_admin = request.user.status >= 7

    if process_self:
        fields |= {
            'phone',
            'mail',
            'social',
            'subscription',
            'pay',
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
            'subscription',
            'pay',
        }

    if data.fields:
        fields = fields & set(data.fields)

    data.fields = data.fields and set(data.fields) | {'id'}

    # Processing
    def handler(user):
        user['online'] = online_back(user['id'])
        return user

    # Get
    users = User.composite(
        ids=data.id,
        count=data.count,
        offset=data.offset,
        fields=fields,
        handler=handler,
    )

    # Response
    return {
        'users': users,
    }
