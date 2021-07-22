"""
The registration method of the account object of the API
"""
from ...funcs import BaseType, validate, online_start, report
from ...models.user import User
from ...models.token import Token
from ...models.action import Action
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
            mail=data.mail,
            mail_verified=False,
            social=data.social,
            actions=[action.json(default=False)],
        )
    except ValueError as e:
        raise ErrorRepeat(e) # TODO: to errors.py

    user.save()

    # Report
    report.important(
        "User registration",
        {
            'user': user.id,
            'token': request.token,
            'network': request.network,
        },
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
