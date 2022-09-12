"""
The authorization via social networks method of the account object of the API
"""

import json
import urllib
import base64

from typing import Union
import requests
from libdev.codes import get_network
from consys.errors import ErrorAccess, ErrorWrong

from api.lib import BaseType, validate, cfg, report
from api.models.user import User
from api.models.token import Token
from api.models.track import Track
from api.methods.account.auth import reg
from api.methods.account.online import online_start


class Type(BaseType):
    social: Union[str, int]
    code: str
    # NOTE: For general authorization method fields
    user: Union[str, int] = None
    login: str = None
    image: str = None
    mail: str = None
    name: str = None
    surname: str = None

# pylint: disable=too-many-branches,too-many-statements
@validate(Type)
async def handle(request, data):
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
                )
            ).text
        )

        if 'user_id' not in response or 'access_token' not in response:
            raise ErrorAccess('code')

        data.user = response['user_id']
        data.mail = response.get('email')
        token = response['access_token']

        # link = 'https://api.vk.com/method/account.getProfileInfo' \
        #        '?access_token={}&v=5.103'
        link = 'https://api.vk.com/method/users.get?user_ids={}&fields=' \
               'photo_max_orig,nickname&access_token={}&v=5.103'

        try:
            response = json.loads(
                requests.get(
                    link.format(data.user, token)
                ).text
            )['response'][0]
        except Exception as e:
            raise ErrorAccess('vk') from e

        data.name = response.get('first_name')
        data.surname = response.get('last_name')
        data.login = response.get('nickname')
        data.image = str(base64.b64encode(
            requests.get(response['photo_max_orig']).content
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
        response = json.loads(requests.post(link, json=cont).text)

        if 'access_token' not in response:
            raise ErrorAccess('code')

        link = 'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'
        response = json.loads(
            requests.get(
                link.format(response['access_token'])
            ).text
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
            requests.get(response['picture']).content
        ))[2:-1] if 'picture' in response else None

    # Wrong ID
    if not data.user:
        await report.warning("Wrong ID", {
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
            token=request.token,
        ).save()

    # Register
    else:
        new = True
        user = await reg(request, data, 'social')

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('auth')

    try:
        token = Token.get(ids=request.token, fields={'user'})
    except ErrorWrong:
        token = Token(id=request.token)

    if token.user and token.user != user.id:
        await report.warning("Reauth", {
            'from': token.user,
            'to': user.id,
            'token': request.token,
        })

    token.user = user.id
    token.save()

    # Update online users
    await online_start(request.sio, request.token)

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }
