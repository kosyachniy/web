"""
The authorization method of the account object of the API
"""

from consys.handlers import process_lower, pre_process_phone, check_phone, \
                            check_mail, process_password
from consys.errors import ErrorInvalid, ErrorWrong, ErrorAccess

from ...lib import BaseType, validate, report
from ...models.user import User
from ...models.token import Token
from ...models.action import Action
from .online import online_start


def detect_type(login):
    """ Detect the type of authorization """

    if check_phone(None, None, pre_process_phone(login)):
        return 'phone'

    if check_mail(None, None, login):
        return 'mail'

    return 'login'

# pylint: disable=too-many-locals,too-many-branches
async def auth(this, request, method, login, password, by):
    """ Authorization / registration in different ways """

    # TODO: Сокет на авторизацию на всех вкладках токена
    # TODO: Перезапись информации этого токена уже в онлайне
    # TODO: Pre-registration data (promos, actions, posts)
    # TODO: without password
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
        'phone',
        'mail',
        'social',
        'status',
    }

    # Authorize

    if by == 'phone':
        handler = pre_process_phone
    else:
        handler = process_lower

    new = False
    login_processed = handler(login)
    users = User.get(fields=fields, **{by: login_processed})

    if users:
        if len(users) > 1:
            await report.warning(
                "More than 1 user",
                {by: login},
            )

        user = users[0]

    else:
        new = True

    # Register
    if new:
        action = Action(
            name='account_reg',
            details={
                'network': request.network,
                'ip': request.ip,
                by: login,
                'password': password,
            },
        )

        if by == 'phone':
            req = {
                'phone': login_processed,
                'phone_verified': False,
            }
        elif by == 'mail':
            req = {
                'mail': login_processed,
                'mail_verified': False,
            }
        else:
            req = {
                'login': login_processed,
            }

        try:
            user = User(
                password=password,
                actions=[action.json(default=False)], # TODO: without `.json()`
                **req,
            )
        except ValueError as e:
            raise ErrorInvalid(e) from e

        user.save()

        # Report
        await report.important(
            f"User registration by {by}",
            {
                'user': user.id,
                by: f"+{login}" if by == 'phone' else login,
                'token': request.token,
                'network': request.network,
                # TODO: ip, geo
            },
            tags=['reg'],
        )

    else:
        # Check password

        password = process_password(password)
        users = User.get(id=user.id, password=password)

        if not users:
            raise ErrorWrong('password')

        # Update

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
        raise ErrorAccess(method)

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

    # TODO: Pre-registration data (promos, actions, posts)

    # Update online users
    await online_start(this.sio, request.token)

    # TODO: redirect to active space
    # if space_id:
    #     for socket_id in Socket(user=user.id):
    #         this.sio.emit('space_return', {
    #             'url': f'/space/{space_id}',
    #         }, room=socket_id)

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }


class Type(BaseType):
    login: str # login / mail / phone
    password: str

@validate(Type)
async def handle(this, request, data):
    """ Sign in / Sign up """

    by = detect_type(data.login)

    return await auth(this, request, 'auth', data.login, data.password, by)
