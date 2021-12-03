"""
The authorization method of the account object of the API
"""

from consys.handlers import process_lower, pre_process_phone, check_phone, \
                            check_mail, process_password
from consys.errors import ErrorWrong, ErrorAccess

from api.lib import BaseType, validate, report
from api.models.user import User
from api.models.token import Token
from api.models.action import Action
from api.models.track import Track
from api.methods.account.online import online_start


def detect_type(login):
    """ Detect the type of authorization """

    if check_phone(None, None, pre_process_phone(login)):
        return 'phone'

    if check_mail(None, None, login):
        return 'mail'

    return 'login'

async def reg(request, data, by, method=None):
    """ Register an account """

    # Action tracking

    details = {
        'type': by,
        'network': request.network,
        'ip': request.ip,
    }

    if by == 'bot':
        details['social_user'] = data.user
        details['social_login'] = data.login
    else:
        details[by] = data.login
        # NOTE: Remove this if no password verification is required
        details['password'] = process_password(data.password)

    if method is not None:
        details['type'] = method

    action = Action(
        title='acc_reg',
        data=details,
    )

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
                'id': request.network, # TODO: Several accounts in one network
                'user': data.user,
                'login': data.login,
                'name': data.name,
                'surname': data.surname,
                'language': request.locale,
            }],
        }
    else:
        req = {
            'login': data.login,
        }

    user = User(
        actions=[action.json(default=False)], # TODO: without `.json()`
        **req,
    )

    # TODO: Subscription

    user.save()

    # Report

    req = {
        'user': user.id,
        'network': request.network,
        'type': method,
        # TODO: ip, geo
    }

    if by=='bot':
        req['login'] = data.login and f"@{data.login}"
    else:
        req[by] = f"+{user.phone}" if by == 'phone' else user.login

    if data.name or data.surname:
        req['name'] = f"{data.name or ''} {data.surname or ''}"

    await report.important(f"User registration by {by}", req, tags=['reg', by])

    return user

async def auth(request, method, data, by):
    """ Authorization / registration in different ways """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)
    # TODO: the same token
    # TODO: Only by token (automaticaly, without any info)

    # No access
    if request.user.status < 2:
        raise ErrorAccess(method)

    # Data preparation
    # TODO: optimize
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

    # Authorize

    if by == 'phone':
        handler = pre_process_phone
    else:
        handler = process_lower

    new = False
    login_processed = handler(data.login)
    users = User.get(fields=fields, **{by: login_processed})

    if users:
        if len(users) > 1:
            await report.warning(
                "More than 1 user",
                {by: data.login},
            )

        user = users[0]

    else:
        new = True

    if new:
        # Register
        user = await reg(request, data, by)

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
                'ip': request.ip,
            },
            user=user.id,
        ).save()

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess(method)

    try:
        token = Token.get(ids=request.token, fields={'user'})
    except ErrorWrong:
        token = Token(id=request.token)

    if token.user and token.user != user.id:
        await report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id, 'token': request.token},
        )

    token.user = user.id
    token.save()

    # TODO: Pre-registration data (promos, actions, posts)

    # Update online users
    await online_start(request.sio, request.token)

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }


class Type(BaseType):
    login: str # login / mail / phone
    # NOTE: Remove this if no password verification is required
    password: str
    # NOTE: For general authorization method fields
    name: str = None
    surname: str = None

@validate(Type)
async def handle(request, data):
    """ Sign in / Sign up """

    by = detect_type(data.login)

    return await auth(request, 'auth', data, by)
