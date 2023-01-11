"""
The authorization via social networks method of the account object of the API
"""

import json
import urllib
import base64
from typing import Union

import jwt
import requests
from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from libdev.codes import get_network
from consys.errors import ErrorAccess, ErrorWrong

from models.user import User
from models.token import Token
from models.track import Track
from routes.account.auth import reg
from routes.account.online import online_start
from lib import cfg, report


router = APIRouter()


class Type(BaseModel):
    social: Union[str, int]
    code: str
    # NOTE: For general authorization method fields
    user: Union[str, int] = None
    login: str = None
    image: str = None
    mail: str = None
    name: str = None
    surname: str = None
    utm: str = None

# pylint: disable=too-many-branches,too-many-statements
@router.post("/social/")
async def handler(
    request: Request,
    data: Type = Body(...),
):
    """ Via social network """

    # TODO: actions
    # TODO: image
    # TODO: the same token
    # TODO: Сшивать профили, если уже есть с такой почтой / ...

    # Preparing params
    data.social = get_network(data.social)

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

    # VK
    if data.social == 3:
        link = 'https://oauth.vk.com/access_token?client_id={}' \
               '&client_secret={}&redirect_uri={}callback&code={}'
        response = json.loads(
            requests.get(
                link.format(
                    cfg('vk.id'),
                    cfg('vk.secret'),
                    cfg('web'),
                    data.code,
                ), timeout=10
            ).text
        )

        if 'user_id' not in response or 'access_token' not in response:
            raise ErrorAccess('code')

        data.user = response['user_id']
        data.mail = response.get('email')
        access_token = response['access_token']

        # link = 'https://api.vk.com/method/account.getProfileInfo' \
        #        '?access_token={}&v=5.103'
        link = 'https://api.vk.com/method/users.get?user_ids={}&fields=' \
               'photo_max_orig,nickname&access_token={}&v=5.103'

        try:
            response = json.loads(
                requests.get(
                    link.format(data.user, access_token), timeout=10
                ).text
            )['response'][0]
        except Exception as e:
            raise ErrorAccess('vk') from e

        data.name = response.get('first_name')
        data.surname = response.get('last_name')
        data.login = response.get('nickname')
        data.image = str(base64.b64encode(
            requests.get(response['photo_max_orig'], timeout=30).content
        ))[2:-1] if 'photo_max_orig' in response else None

    # Google
    elif data.social == 4:
        link = 'https://accounts.google.com/o/oauth2/token'
        cont = {
            'client_id': cfg('google.id'),
            'client_secret': cfg('google.secret'),
            'redirect_uri': f"{cfg('web')}callback",
            'grant_type': 'authorization_code',
            'code': urllib.parse.unquote(data.code),
        }
        response = json.loads(requests.post(link, json=cont, timeout=10).text)

        if 'access_token' not in response:
            raise ErrorAccess('code')

        link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'
        response = json.loads(
            requests.get(link.format(response['access_token']), timeout=10).text
        )

        if 'id' not in response:
            raise ErrorAccess('code')

        data.user = response['id']

        # link = 'https://www.googleapis.com/oauth2/v1/userinfo' \
        #        '?access_token={}'.format(data.data['access_token'])
        # res_google = json.loads(requests.get(link).text)

        data.name = response.get('given_name')
        data.surname = response.get('family_name')
        data.mail = response.get('email')
        data.image = str(base64.b64encode(
            requests.get(response['picture'], timeout=30).content
        ))[2:-1] if 'picture' in response else None

    # Wrong ID
    if not data.user:
        await report.error("Wrong ID", {
            'social': data.social,
            'social_user': data.user,
        })
        raise ErrorWrong('id')

    users = User.get(social={'$elemMatch': {
        'id': data.social,
        'user': data.user,
    }}, fields=fields)

    if len(users) > 1:
        await report.warning("More than 1 user", {
            'social': data.social,
            'social_user': data.user,
        })

    elif len(users):
        new = False
        user = users[0]

        # Action tracking
        Track(
            title='acc_auth',
            data={
                'type': 'social',
                'social': data.social,
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
            'social',
        )

    # Assignment of the token to the user

    if not request.state.token:
        raise ErrorAccess('auth')

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

    # Update online users
    await online_start(token.id)

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
