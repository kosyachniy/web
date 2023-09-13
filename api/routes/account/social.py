"""
The authorization via social networks method of the account object of the API
"""

import json
import urllib

import jwt
import requests
from fastapi import APIRouter, Body, Request
from pydantic import BaseModel
from libdev.codes import get_network
# pylint: disable=import-error
from libdev.img import convert
from libdev.s3 import upload_file
from consys.errors import ErrorAccess, ErrorWrong

from routes.account.auth import auth
from lib import cfg, report


router = APIRouter()


def auth_telegram(data):
    """ Authorization via Telegram """
    data.user = jwt.decode(data.code, cfg('jwt'), algorithms='HS256')['user']
    return data, lambda: None

def auth_google(data):
    """ Authorization via Google """

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
    data.name = response.get('given_name')
    data.surname = response.get('family_name')
    data.mail = response.get('email')

    def loader_image():
        return upload_file(convert(response.get('picture')), file_type='webp')

    return data, loader_image


class Type(BaseModel):
    social: str | int
    code: str
    # NOTE: For general authorization method fields
    user: str | int = None
    login: str = None
    image: str = None
    mail: str = None
    name: str = None
    surname: str = None
    utm: str = None

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

    # TODO: VK
    if data.social == 2:
        data, loader_image = auth_telegram(data)
    elif data.social == 4:
        data, loader_image = auth_google(data)

    # Wrong ID
    if not data.user:
        await report.error("Wrong ID", {
            'social': data.social,
            'social_user': data.user,
        })
        raise ErrorWrong('id')

    return await auth(request, data, 'social', {
        'social': {
            '$elemMatch': {
                'id': data.social,
                'user': data.user,
            },
        },
    }, online=True, loader_image=loader_image)
