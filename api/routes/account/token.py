"""
The token creating method of the account object of the API
"""

import jwt
from fastapi import APIRouter, Body #, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
# from libdev.gen import generate
from libdev.codes import get_network
from consys.errors import ErrorWrong

from lib import cfg
from models.token import Token


router = APIRouter()


class Type(BaseModel):
    token: str
    network: str
    utm: str = None

@router.post("/token/")
async def handler(
    data: Type = Body(...),
    # ip = Depends(get_ip),
):
    """ Create token """

    network = get_network(data.network)

    # Get
    try:
        token = Token.get(ids=data.token, fields={'user'})

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
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, cfg('jwt'), algorithm='HS256')

    # Response
    response = JSONResponse(content={
        'token': token,
    })
    response.set_cookie(key="Authorization", value=token)
    return response
