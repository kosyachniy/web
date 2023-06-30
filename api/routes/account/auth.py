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
from consys.errors import ErrorWrong

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

# pylint: disable=too-many-branches,too-many-statements
async def reg(network, ip, locale, token_id, data, by, method=None):
    """ Register an account """

    # Action tracking

    details = {
        'type': by,
        'network': network,
        'locale': locale,
    }

    if data.utm:
        details['utm'] = data.utm
    else:
        token = Token.get(token_id, fields={'utm'})
        if token.utm:
            details['utm'] = token.utm

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
        locale=locale,
        image=data.image,
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
        token=token_id,
        ip=ip,
    ).save()

    # Report

    req = {
        'user': user.id,
        'network': NETWORKS[network].upper(),
        'type': method,
        'utm': data.utm,
        'ip': ip,
        # TODO: geo by ip
        'locale': locale,
    }

    if by == 'bot':
        req['login'] = data.login and f"@{data.login}"
    elif by == 'social':
        req['social'] = NETWORKS[data.social].upper()
        req['login'] = data.login and f"@{data.login}"
        req['mail'] = data.mail
    elif by == 'phone':
        req['phone'] = f"+{user.phone}"
    elif by == 'mail':
        req['mail'] = user.mail
    else:
        req[by] = user.login

    if data.name or data.surname:
        req['name'] = f"{data.name or ''} {data.surname or ''}"

    await report.important(f"User registration by {by}", req, tags=['reg', by])

    return user

async def auth(
    request,
    data,
    by,
    conditions,
    online=False,
    password=False,
    loader_image=lambda: None,
):
    """ Authorization / registration in different ways """

    # TODO: auth all tabs with this token via web sockets
    # TODO: pre-registration data: promo, tracking, posts
    # TODO: uniq token
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

    users = User.get(fields=fields, **conditions)

    if len(users) > 1:
        new = False
        user = users[0]

        if by == 'social':
            req = {
                'social': data.social,
                'social_user': data.user,
            }
        elif by == 'bot':
            req = {
                'network': request.state.network,
                'social_user': data.user,
                'social_login': data.login,
            }
        elif by == 'app':
            req = {
                'network': request.state.network,
                'social_user': data.user,
            }
        elif by == 'mail':
            req = {
                by: data.mail,
            }
        else:
            req = {
                by: data.login,
            }

        await report.warning("More than 1 user", req)

    elif len(users):
        new = False
        user = users[0]

        # Check password
        if password:
            password = process_password(data.password)
            users = User.get(id=user.id, password=password, fields={})
            if not users:
                raise ErrorWrong('password')

        req = {
            'type': by,
        }
        if by == 'social':
            req['social'] = data.social
        elif by in {'bot', 'app'}:
            req['network'] = request.state.network
        else:
            req['ip'] = request.state.ip

        # Action tracking
        Track(
            title='acc_auth',
            data=req,
            user=user.id,
            token=request.state.token,
            ip=request.state.ip,
        ).save()

    # Register
    else:
        # Image
        image = loader_image()
        if image:
            data.image = image

        new = True
        user = await reg(
            request.state.network,
            request.state.ip,
            request.state.locale,
            request.state.token,
            data,
            by,
        )

    # Assignment of the token to the user
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

    # TODO: Pre-registration data (promos, actions, posts)

    # Update online users
    if online:
        await online_start(token.id)

    # JWT
    token = jwt.encode({
        'token': token.id,
        'user': user.id,
        'network': request.state.network,
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


class Type(BaseModel):
    login: str # login / mail / phone
    # NOTE: Remove this if no password verification is required
    password: str
    # NOTE: For general authorization method fields
    name: str = None
    surname: str = None
    image: str = None
    utm: str = None

@router.post("/auth/")
async def handler(
    request: Request,
    data: Type = Body(...),
):
    """ Sign in / Sign up """

    by = detect_type(data.login)
    if by == 'phone':
        handle = pre_process_phone
    else:
        handle = process_lower

    login_processed = handle(data.login)
    return await auth(request, data, by, {
        by: login_processed,
    }, online=True, password=True)
