"""
The authorization via mini app method of the account object of the API
"""

import hashlib
from collections import OrderedDict
from base64 import b64encode
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from consys.errors import ErrorWrong, ErrorInvalid
import jwt

from models.user import User
from models.track import Track
from services.auth import auth
from routes.account.auth import reg
from lib import cfg, report


router = APIRouter()


def is_valid_vk(*, query: dict) -> bool:
    """ Check url """

    vk_subset = OrderedDict(sorted(
        x for x in query.items() if x[0][:3] == 'vk_'
    ))
    hash_code = b64encode(HMAC(
        cfg('vk.secret').encode(),
        urlencode(vk_subset, doseq=True).encode(),
        hashlib.sha256
    ).digest())
    decoded_hash_code = hash_code.decode('utf-8')[:-1] \
                                 .replace('+', '-') \
                                 .replace('/', '_')

    return query['sign'] == decoded_hash_code

class Type(BaseModel):
    url: str
    referral: str = None
    # NOTE: For general authorization method fields
    user: str = None
    login: str = None
    password: str = None
    name: str = None
    surname: str = None
    utm: str = None

@router.post("/app/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(auth),
):
    """ Mini app auth """

    try:
        params = dict(parse_qsl(
            urlparse(data.url).query,
            keep_blank_values=True,
        ))
        data.user = int(params['vk_user_id'])
        status = is_valid_vk(query=params)
    except Exception as e:
        await report.warning("Failed authorization attempt in the app", {
            'url': data.url,
            'user': user.id,
            'network': request.state.network,
            'error': e,
        })
        raise ErrorInvalid('url') from e

    if not status:
        raise ErrorWrong('url')

    #

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
        })

    elif len(users):
        new = False
        user = users[0]

        # Action tracking
        Track(
            title='acc_auth',
            data={
                'type': 'app',
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
            'app',
        )

    # JWT
    token = jwt.encode({
        'token': request.state.token,
        'user': user.id,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, cfg('jwt'), algorithm='HS256')

    # # Referral
    # if data.referral:
    #     user.referral = data.referral
    #     user.save()

    # Response
    response = JSONResponse(content={
        **user.json(fields=fields),
        'new': new,
        'token': token,
    })
    response.set_cookie(key="Authorization", value=f"Bearer {token}")
    return response
