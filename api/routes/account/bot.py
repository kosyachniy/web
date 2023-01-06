"""
The authorization via social networks method of the account object of the API
"""

import jwt
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from consys.errors import ErrorWrong, ErrorAccess

from lib import cfg, report
from models.user import User # process_lower
from models.token import Token
from models.track import Track
from services.request import get_request
from services.auth import get_token
from routes.account.auth import reg


router = APIRouter()


class Type(BaseModel):
    user: int
    login: str = None
    name: str = None
    surname: str = None
    utm: str = None

@router.post("/bot/")
async def handler(
    data: Type = Body(...),
    request = Depends(get_request),
    token = Depends(get_token),
):
    """ By bot """

    # TODO: image
    # TODO: the same token
    # TODO: block by token

    fields = {
        'id',
        'login',
        'image',
        'name',
        'surname',
        'title',
        'phone',
        'mail',
        'social',
        'status',
        # 'subscription',
        # 'balance',
    }

    users = User.get(social={'$elemMatch': {
        'id': request.network,
        'user': data.user,
    }}, fields=fields)

    if len(users) > 1:
        await report.warning("More than 1 user", {
            'network': request.network,
            'social_user': data.user,
            'social_login': data.login,
        })

    elif len(users):
        new = False
        user = users[0]

        # Action tracking
        Track(
            title='acc_auth',
            data={
                'type': 'bot',
                'network': request.network,
            },
            user=user.id,
            token=token,
        ).save()

    # Register
    else:
        new = True
        user = await reg(request, token, data, 'bot')

    # Assignment of the token to the user

    if not token:
        raise ErrorAccess('auth')

    try:
        token = Token.get(token, fields={'user'})
    except ErrorWrong:
        token = Token(id=token)

    if token.user and token.user != user.id:
        await report.warning("Reauth", {
            'from': token.user,
            'to': user.id,
            'token': token.id,
        })

    token.user = user.id
    token.save()

    # JWT
    token = jwt.encode({
        'token': token.id,
        'user': user.id,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, cfg('jwt'), algorithm='HS256')

    # Response
    response = JSONResponse(content={
        **user.json(fields=fields),
        'new': new,
        'token': token,
    })
    response.set_cookie(key="Authorization", value=f"Bearer {token}")
    return response
