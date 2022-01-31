"""
The authorization via mini app method of the account object of the API
"""

import datetime
import hashlib
from collections import OrderedDict
from base64 import b64encode
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode

from consys.errors import ErrorWrong, ErrorInvalid
# pylint: disable=import-error
import jwt

from api.lib import BaseType, validate, cfg, report
from api.models.user import User
from api.models.track import Track
from api.methods.account.auth import reg


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


class Type(BaseType):
    url: str
    referral: str = None
    # NOTE: For general authorization method fields
    user: str = None
    login: str = None
    password: str = None
    name: str = None
    surname: str = None

@validate(Type)
async def handle(request, data):
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
            'user': request.user.id,
            'network': request.network,
            'error': e,
        })
        raise ErrorInvalid('url') from e

    if not status:
        raise ErrorWrong('url')

    # JWT
    token = jwt.encode({
        'user': data.user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, cfg('jwt')).decode('UTF-8')

    #

    fields = {
        'id',
        'login',
        'avatar',
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
        })

    elif len(users):
        new = False
        user = users[0]

        # Action tracking
        Track(
            title='acc_auth',
            data={
                'type': 'app',
                'network': request.network,
            },
            user=user.id,
        ).save()

    # Register
    else:
        new = True
        user = await reg(request, data, 'app')

    # # Referral
    # if data.referral:
    #     user.referral = data.referral
    #     user.save()

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
        'token': token,
    }
