"""
The token creating method of the account object of the API
"""

import jwt
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from libdev.codes import get_network
from consys.errors import ErrorWrong

from models.token import Token
from lib import cfg


router = APIRouter()


class Type(BaseModel):
    token: str
    network: str
    utm: str = None

@router.post("/token/")
async def handler(
    data: Type = Body(...),
):
    """ Create token """

    # TODO: ip

    network = get_network(data.network)

    # Get
    try:
        token = Token.get(data.token, fields={'user'})

    # Create
    except ErrorWrong:
        token = Token(
            id=data.token, # generate(),
            network=network,
            utm=data.utm,
        )
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
