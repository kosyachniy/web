"""
The registration method of the account object of the API
"""

from consys.errors import ErrorAccess, ErrorInvalid

from ...lib.types import BaseType, validate
from ...lib.reports import report
from ...models.user import User
from ...models.token import Token
from ...models.action import Action
from .online import online_start


class Type(BaseType):
    login: str = None
    password: str = None
    avatar: str = None
    name: str = None
    surname: str = None
    phone: str = None
    mail: str = None
    social: list[dict] = None

@validate(Type)
async def handle(this, request, data):
    """ Sign up """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)

    # No access
    if request.user.status < 2:
        raise ErrorAccess('reg')

    # Create

    action = Action(
        name='account_reg',
        details={
            'network': request.network,
            'ip': request.ip,
            'login': data.login,
            'name': data.name,
            'surname': data.surname,
            'phone': data.phone,
            'mail': data.mail,
            'social': data.social,
            'password': data.password,
        },
    )

    try:
        user = User(
            login=data.login,
            password=data.password,
            avatar=data.avatar,
            name=data.name,
            surname=data.surname,
            phone=data.phone,
            mail=data.mail,
            mail_verified=False,
            social=data.social,
            actions=[action.json(default=False)],
        )
    except ValueError as e:
        raise ErrorInvalid(e) from e # TODO: or ErrorRepeat, to errors.py

    user.save()

    # Report
    await report.important(
        "User registration by login",
        {
            'user': user.id,
            'login': data.login,
            'name': f"{data.name or ''} {data.surname or ''}",
            'phone': data.phone and f"+{data.phone}",
            'mail': data.mail,
            'social': data.social,
            'token': request.token,
            'network': request.network,
            # TODO: ip, geo
        },
        tags=['reg'],
    )

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('token')

    token = Token(
        id=request.token,
        user=user.id,
    )

    token.save()

    # Update online users
    await online_start(this.sio, request.token)

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
