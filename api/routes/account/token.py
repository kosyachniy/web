"""
The token creating method of the account object of the API
"""

import jwt
from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from libdev.codes import get_network
from libdev.dev import check_public_ip
from consys.errors import ErrorWrong

from models.token import Token
from lib import cfg


router = APIRouter()


class Type(BaseModel):
    token: str
    network: str
    utm: str = None
    extra: dict = None

@router.post("/token/")
async def handler(
    request: Request,
    data: Type = Body(...),
):
    """ Create token """

    # TODO: ip

    network = get_network(data.network)
    save = False

    # Get
    try:
        token = Token.get(data.token)

    # Create
    except ErrorWrong:
        token = Token(
            id=data.token, # generate(),
        )
        save = True

    # Attach data
    if not token.network and network:
        token.network = network
        save = True
    if not token.utm and data.utm:
        token.utm = data.utm
        save = True
    ip = check_public_ip(request.state.ip)
    if not token.ip and ip:
        token.ip = ip
        save = True
    if not token.locale and request.state.locale:
        token.locale = request.state.locale
        save = True
    if not token.user_agent and request.state.user_agent:
        token.user_agent = request.state.user_agent
        save = True
    if not token.extra and data.extra:
        token.extra = data.extra
        save = True
    if save:
        token.save()

    # JWT
    token = jwt.encode({
        'token': token.id,
        'user': token.user,
        'network': network,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, cfg('jwt'), algorithm='HS256')

    # Response
    response = JSONResponse(content={
        'token': token,
    })
    response.set_cookie(key="Authorization", value=f"Bearer {token}")
    return response
