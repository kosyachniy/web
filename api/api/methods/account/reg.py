"""
The registration method of the account object of the API
"""

import sys

from ...funcs import check_params, online_start, report
from ...models.user import User
from ...models.token import Token
from ...errors import ErrorAccess, ErrorRepeat


async def handle(this, **x):
    """ Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне

    # Checking parameters

    x = check_params(x, (
        ('login', False, str),
        ('password', False, str),
        ('name', False, str),
        ('surname', False, str),
        ('avatar', False, str),
        ('file', False, str),
        ('mail', False, str),
        ('social', False, list, dict),
    ))

    # Create

    try:
        user = User(
            login=x['login'],
            password=x['password'],
            avatar=x['avatar'],
            name=x['name'],
            surname=x['surname'],
            mail=x['mail'],
            mail_verified=False,
            social=x['social'],
        )
    except ValueError as e:
        type_, value, traceback = sys.exc_info() # TODO: to errors.py
        raise ErrorRepeat(str(value))

    user.save()

    # Report
    report.important(
        "User registration",
        {'user': user.id, 'token': this.token},
        path='methods.account.reg',
    )

    # Assignment of the token to the user

    if not this.token:
        raise ErrorAccess('token')

    token = Token(
        id=this.token,
        user=user.id,
    )

    token.save()

    # Update online users

    await online_start(this.sio, this.token)

    # Response

    res = {
        'id': user.id,
        'login': user.login,
        'avatar': user.avatar,
        'name': user.name,
        'surname': user.surname,
        'mail': user.mail,
        'status': user.status,
        'new': True,
    }

    return res
