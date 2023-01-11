"""
The authorization method of the account object of the API
"""

import jwt
from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from libdev.codes import NETWORKS
from consys.handlers import (
    process_lower, pre_process_phone, check_phone, check_mail, process_password,
)
from consys.errors import ErrorWrong, ErrorAccess

from models.user import User
from models.token import Token
from models.track import Track
from routes.account.online import online_start
from lib import cfg, report


router = APIRouter()


def detect_type(login):
    """ Detect the type of authorization """

    if check_phone(None, None, pre_process_phone(login)):
        return 'phone'

    if check_mail(None, None, login):
        return 'mail'

    return 'login'

# pylint: disable=too-many-branches
async def reg(network, ip, locale, token, data, by, method=None):
    """ Register an account """

    # Action tracking

    details = {
        'type': by,
        'network': network,
        'ip': ip,
    }

    if data.utm:
        details['utm'] = data.utm

    if by == 'bot':
        details['social_user'] = data.user
        details['social_login'] = data.login
    elif by == 'social':
        details['social'] = data.social
        details['social_user'] = data.user
        details['social_login'] = data.login
        details['mail'] = data.mail
    elif by == 'app':
        details['social_user'] = data.user
    else:
        details[by] = data.login
        # NOTE: Remove this if no password verification is required
        details['password'] = process_password(data.password)

    if method is not None:
        details['type'] = method

    # Create user

    if by == 'phone':
        req = {
            'phone': data.login,
            'phone_verified': False,
            # NOTE: Remove this if no password verification is required
            'password': data.password,
        }
    elif by == 'mail':
        req = {
            'mail': data.login,
            'mail_verified': False,
            # NOTE: Remove this if no password verification is required
            'password': data.password,
        }
    elif by == 'bot':
        req = {
            'arg_ignore': {'login', 'name', 'surname'},
            'login': data.login or None,
            'name': data.name or None,
            'surname': data.surname or None,
            'social': [{
                'id': network, # TODO: Several accounts in one network
                'user': data.user,
                'login': data.login,
                'name': data.name,
                'surname': data.surname,
                'locale': locale,
            }],
        }
    elif by == 'social':
        req = {
            'arg_ignore': {'login', 'mail', 'name', 'surname'},
            'login': data.login or None,
            'mail': data.mail or None,
            'name': data.name or None,
            'surname': data.surname or None,
            'social': [{
                'id': data.social, # TODO: Several accounts in one network
                'user': data.user,
                'login': data.login,
                'mail': data.mail,
                'name': data.name,
                'surname': data.surname,
            }],
        }
    elif by == 'app':
        req = {
            'social': [{
                'id': network, # TODO: Several accounts in one network
                'user': data.user,
            }],
        }
    else:
        req = {
            'login': data.login,
        }

    user = User(
        utm=data.utm,
        **req,
    )

    # TODO: Preauth data
    # TODO: Subscription

    user.save()

    # Action tracking
    Track(
        title='acc_reg',
        data=details,
        user=user.id,
        token=token,
    ).save()

    # Report

    req = {
        'user': user.id,
        'network': NETWORKS[network].upper(),
        'type': method,
        'utm': data.utm,
        # TODO: ip, geo
    }

    if by == 'bot':
        req['login'] = data.login and f"@{data.login}"
    elif by == 'social':
        req['social'] = NETWORKS[data.social].upper()
        req['login'] = data.login and f"@{data.login}"
        req['mail'] = data.mail
    elif by == 'phone':
        req['phone'] = f"+{user.phone}"
    else:
        req[by] = user.login

    if data.name or data.surname:
        req['name'] = f"{data.name or ''} {data.surname or ''}"

    await report.important(f"User registration by {by}", req, tags=['reg', by])

    return user

async def auth(network, ip, locale, token, method, data, by):
    """ Authorization / registration in different ways """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)
    # TODO: the same token
    # TODO: Only by token (automaticaly, without any info)
    # TODO: block by token

    # Data preparation
    # TODO: optimize
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

    # Authorize

    if by == 'phone':
        handle = pre_process_phone
    else:
        handle = process_lower

    new = False
    login_processed = handle(data.login)
    users = User.get(fields=fields, **{by: login_processed})

    if users:
        if len(users) > 1:
            await report.warning("More than 1 user", {
                by: data.login,
            })

        user = users[0]

    else:
        new = True

    if new:
        # Register
        user = await reg(network, ip, locale, token, data, by)

    else:
        # NOTE: Remove this if no password verification is required
        # Check password
        password = process_password(data.password)
        users = User.get(id=user.id, password=password, fields={})
        if not users:
            raise ErrorWrong('password')

        # Action tracking
        Track(
            title='acc_auth',
            data={
                'type': by,
                'ip': ip,
            },
            user=user.id,
            token=token,
        ).save()

    # Assignment of the token to the user

    try:
        token = Token.get(token, fields={'user'})
    except ErrorWrong:
        token = Token(id=token)

    if token.user and token.user != user.id:
        await report.warning("Reauth", {
            'from': token.user,
            'to': user.id,
            'token': token.id,
        })

    token.user = user.id
    token.save()

    # TODO: Pre-registration data (promos, actions, posts)

    # Update online users
    await online_start(token.id)

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }


class Type(BaseModel):
    login: str # login / mail / phone
    # NOTE: Remove this if no password verification is required
    password: str
    # NOTE: For general authorization method fields
    name: str = None
    surname: str = None
    utm: str = None

@router.post("/auth/")
async def handler(
    request: Request,
    data: Type = Body(...),
):
    """ Sign in / Sign up """

    by = detect_type(data.login)
    data = await auth(
        request.state.network,
        request.state.ip,
        request.state.locale,
        request.state.token,
        'auth',
        data,
        by,
    )

    # JWT
    token = jwt.encode({
        'token': request.state.token,
        'user': data['id'],
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }, cfg('jwt'), algorithm='HS256')

    # Response
    response = JSONResponse(content={
        **data,
        'token': token,
    })
    response.set_cookie(key="Authorization", value=f"Bearer {token}")
    return response
