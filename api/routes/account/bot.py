"""
The authorization via social networks method of the account object of the API
"""

import jwt
from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from consys.errors import ErrorWrong

from models.user import User # process_lower
from models.token import Token
from models.track import Track
from routes.account.auth import reg
from lib import cfg, report


router = APIRouter()


class Type(BaseModel):
    user: int
    login: str = None
    name: str = None
    surname: str = None
    utm: str = None

@router.post("/bot/")
async def handler(
    request: Request,
    data: Type = Body(...),
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
        'id': request.state.network,
        'user': data.user,
    }}, fields=fields)

    if len(users) > 1:
        await report.warning("More than 1 user", {
            'network': request.state.network,
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
                'network': request.state.network,
            },
            user=user.id,
            token=request.state.token,
        ).save()

    # Register
    else:
        new = True
        user = await reg(
            request.state.network,
            request.state.ip,
            request.state.locale,
            request.state.token,
            data,
            'bot',
        )

    # Assignment of the token to the user

    try:
        token = Token.get(request.state.token, fields={'user'})
    except ErrorWrong:
        token = Token(id=request.state.token)

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
