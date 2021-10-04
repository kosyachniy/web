"""
The authorization method of the account object of the API
"""

from consys.errors import ErrorInvalid, ErrorWrong, ErrorAccess

from ...lib import BaseType, validate, report
from ...models.user import User, process_lower, pre_process_phone, \
                           process_password
from ...models.token import Token
from ...models.action import Action
from .online import online_start


class Type(BaseType):
    login: str # login / mail / phone
    password: str

# pylint: disable=too-many-statements,too-many-branches
@validate(Type)
async def handle(this, request, data):
    """ Sign in / Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)
    # TODO: without password
    # TODO: the same token
    # TODO: Only by token (automaticaly, without any info)

    # No access
    if request.user.status < 2:
        raise ErrorAccess('auth')

    # Data preparation
    # TODO: optimize
    fields = {
        'id',
        'login',
        'avatar',
        'name',
        'surname',
        'phone',
        'mail',
        'social',
        'status',
    }

    # Authorize

    new = False

    try:
        login = process_lower(data.login)
        user = User.get(login=login, fields=fields)[0]
    except ErrorWrong:
        new = True

    if new:
        try:
            mail = process_lower(data.login)
            user = User.get(mail=mail, fields=fields)[0]
        except ErrorWrong:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(data.login)
            user = User.get(phone=phone, fields=fields)[0]
        except ErrorWrong:
            pass
        else:
            new = False

    # Check password
    if not new:
        password = process_password(data.password)
        users = User.get(id=user.id, password=password)

        if not users:
            raise ErrorWrong('password')

    # Register
    if new:
        action = Action(
            name='account_reg',
            details={
                'network': request.network,
                'ip': request.ip,
                'mail': data.login,
                'password': data.password,
            },
        )

        try:
            user = User(
                password=data.password,
                mail=data.login, # TODO: login # TODO: phone
                mail_verified=False,
                actions=[action.json(default=False)], # TODO: without `.json()`
            )
        except ValueError as e:
            raise ErrorInvalid(e) from e

        user.save()

        # Report
        await report.important(
            "User registration by mail",
            {
                'user': user.id,
                'mail': data.login,
                'token': request.token,
                'network': request.network,
                # TODO: ip, geo
            },
            tags=['reg'],
        )

    # Update
    else:
        action = Action(
            name='account_auth',
            details={
                'ip': request.ip,
            },
        )

        user.actions.append(action.json(default=False))
        user.save()

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('auth')

    try:
        token = Token.get(ids=request.token, fields={'user'})
    except ErrorWrong:
        token = Token(id=request.token)

    if token.user:
        await report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id, 'token': request.token},
        )

    token.user = user.id
    token.save()

    # Update online users
    await online_start(this.sio, request.token)

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }
