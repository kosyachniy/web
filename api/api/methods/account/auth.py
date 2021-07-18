"""
The authorization method of the account object of the API
"""

from ...funcs import BaseType, validate, online_start, report
from ...models.user import User, process_login, process_lower, \
                           pre_process_phone, process_password
from ...models.token import Token
from ...models.action import Action
from ...errors import ErrorInvalid, ErrorWrong, ErrorAccess


class Type(BaseType):
    login: str # login / mail / phone
    password: str

@validate(Type)
async def handle(this, request, data):
    """ Sign in / Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)
    # TODO: without password

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
        login = process_login(data.login)
        user = User.get(login=login, fields=fields)[0]
    except:
        new = True

    if new:
        try:
            mail = process_lower(data.login)
            user = User.get(mail=mail, fields=fields)[0]
        except:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(data.login)
            user = User.get(phone=phone, fields=fields)[0]
        except:
            pass
        else:
            new = False

    # Check password
    if not new:
        password = process_password(data.password)

        try:
            User.get(id=user.id, password=password)
        except:
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
            user_data = User(
                password=data.password,
                mail=data.login, # TODO: login
                mail_verified=False,
                actions=[action.json(default=False)],
            )
        except ValueError as e:
            raise ErrorInvalid(e)

        user_data.save()
        user_id = user_data.id

        user = User.get(ids=user_id, fields=fields)

        # Report
        report.important(
            "User registration by mail",
            {
                'user': user_id,
                'token': request.token,
                'network': request.network,
            },
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
    except:
        token = Token(id=request.token)

    if token.user:
        report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id, 'token': request.token},
        )

    token.user = user.id
    token.save()

    # Update online users
    await online_start(this.sio, request.token)

    # Response
    # TODO: del None
    return {
        **user.json(fields=fields),
        'new': new,
    }
