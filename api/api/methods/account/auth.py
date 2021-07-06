"""
The authorization method of the account object of the API
"""

from ...funcs import BaseType, validate, online_start, report
from ...models.user import User, process_login, process_lower, \
                           pre_process_phone, process_password
from ...models.token import Token
from ...errors import ErrorWrong, ErrorAccess


class Type(BaseType):
    login: str # login / mail / phone
    password: str

@validate(Type)
async def handle(this, request):
    """ Sign in / Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)

    # Data preparation

    # TODO: None / not ''
    # if 'password' in x and not request.password:
    #     del request.password

    fields = {
        'login',
        'avatar',
        'name',
        'surname',
        'mail',
        'status',
    } # TODO: optimize

    # Authorize

    new = False

    try:
        login = process_login(request.login)
        user = User.get(login=login, fields=fields)[0]
    except:
        new = True

    if new:
        try:
            mail = process_lower(request.login)
            user = User.get(mail=mail, fields=fields)[0]
        except:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(request.login)
            user = User.get(phone=phone, fields=fields)[0]
        except:
            pass
        else:
            new = False

    if not new:
        password = process_password(request.password)

        try:
            User.get(id=user.id, password=password)
        except:
            raise ErrorWrong('password')

    # Register
    if new:
        user_data = User(
            password=request.password,
            mail=request.login, # TODO: login
            mail_verified=False,
        )
        user_data.save()
        user_id = user_data.id

        user = User.get(ids=user_id, fields=fields)

        # Report
        report.important(
            "User registration by mail",
            {'user': user_id, 'token': this.token},
            path='methods.account.auth',
        )

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('auth')

    if new and this.user.status > 2:
        token = Token.get(ids=this.token, fields={'user'})

        report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id, 'token': this.token},
            path='methods.account.auth',
        )

        token.user = user.id

    else:
        token = Token(
            id=this.token,
            user=user.id,
        )

    token.save()

    # Update online users
    await online_start(this.sio, this.token)

    # Response
    # TODO: del None
    return {
        **user.json(fields={
            'id',
            'login',
            'avatar',
            'name',
            'surname',
            'mail',
            'status',
        }),
        'new': new,
    }
