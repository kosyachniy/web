"""
The getting method of the user object of the API
"""

import time
from typing import Union

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess, ErrorInvalid

from models.user import User
from models.socket import Socket
from services.request import get_request


router = APIRouter()


def online_back(user_id):
    """ Checking how long has been online """

    sockets = Socket.get(user=user_id, fields={})

    if sockets:
        return 0

    user = User.get(user_id, fields={'last_online'})

    if not user.last_online:
        return 0

    return int(time.time() - user.last_online)


class Type(BaseModel):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    fields: list[str] = None

@router.post("/get/")
async def handler(
    data: Type = Body(...),
    request = Depends(get_request),
):
    """ Get """

    # TODO: cursor

    # Checks

    if (
        request.user.status < 4 # TODO: 5
        and data.id != request.user.id
    ):
        raise ErrorAccess('get')

    if request.user.id == 0:
        raise ErrorInvalid('id')

    # TODO: Get myself
    # if not data.id and request.user.id:
    #     data.id = request.user.id

    # Fields
    # TODO: right to roles

    fields = {
        'id',
        'login',
        'image',
        'name',
        'surname',
        'title',
        'status',
        # 'subscription',
        # 'balance',
        'rating',
        'description',
        'discount',
    }

    process_self = data.id == request.user.id
    process_admin = request.user.status >= 7

    if process_self:
        fields |= {
            'phone',
            'mail',
            'social',
            'subscription',
            'pay',
        }

    if process_admin:
        fields |= {
            'phone',
            'mail',
            'social',
            'subscription',
            'pay',
        }

    if data.fields:
        fields = fields & set(data.fields) | {'id'}

    # Processing
    def handle(user):
        if data.fields and 'online' in data.fields:
            user['online'] = online_back(user['id'])

        return user

    # Get
    users = User.complex(
        ids=data.id,
        count=data.count,
        offset=data.offset,
        fields=fields,
        handler=handle,
    )

    # Response
    return {
        'users': users,
    }