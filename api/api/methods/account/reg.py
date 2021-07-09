"""
The registration method of the account object of the API
"""

from ...funcs import BaseType, validate, online_start, report
from ...models.user import User
from ...models.token import Token
from ...errors import ErrorAccess, ErrorRepeat


class Type(BaseType):
    login: str = None
    password: str = None
    avatar: str = None
    name: str = None
    surname: str = None
    mail: str = None
    social: list[dict] = None

@validate(Type)
async def handle(this, request):
    """ Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)

    # No access
    if this.user.status < 2:
        raise ErrorAccess('reg')

    # Create

    try:
        user = User(
            login=request.login,
            password=request.password,
            avatar=request.avatar,
            name=request.name,
            surname=request.surname,
            mail=request.mail,
            mail_verified=False,
            social=request.social,
        )
    except ValueError as e:
        raise ErrorRepeat(e.args[0]) # TODO: to errors.py

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
    return {
        **user.json(fields={
            'id',
            'login',
            'avatar',
            'name',
            'surname',
            'phone',
            'mail',
            'social',
            'status',
        }),
        'new': True,
    }
