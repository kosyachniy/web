"""
The authorization via mini app method of the account object of the API
"""

import hashlib
from collections import OrderedDict
from base64 import b64encode
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from fastapi import APIRouter, Body, Depends, Request
from pydantic import BaseModel
from consys.errors import ErrorWrong, ErrorInvalid

from services.auth import sign
from routes.account.auth import auth
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
    image: str = None
    utm: str = None

@router.post("/app/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
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

    return await auth(request, data, 'app', {
        'social': {
            '$elemMatch': {
                'id': request.state.network,
                'user': data.user,
            },
        },
    })
