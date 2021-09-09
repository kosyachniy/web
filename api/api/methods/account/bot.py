"""
The authorization via social networks method of the account object of the API
"""

from ...funcs import BaseType, validate, report
from ...models.user import User, process_lower
from ...models.token import Token
from ...models.action import Action
from ...errors import ErrorAccess


class Type(BaseType):
    user: int
    login: str = None
    name: str = None
    surname: str = None

# pylint: disable=unused-argument
@validate(Type)
async def handle(this, request, data):
    """ By bot """

    # TODO: avatar
    # TODO: the same token

    # No access
    if request.user.status < 2:
        raise ErrorAccess('social')

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

    users = User.get(social={'$elemMatch': {
        'id': request.network,
        'user': data.user,
    }}, fields=fields)

    if len(users) > 1:
        await report.warning(
            "More than 1 user",
            {
                'network': request.network,
                'social_user': data.user,
                'social_login': data.login,
            },
        )

    elif len(users):
        new = False
        user = users[0]

        action = Action(
            name='account_auth',
            details={
                'network': request.network,
            },
        )

        user.actions.append(action.json(default=False))
        user.save()

    # Register
    else:
        new = True

        action = Action(
            name='account_reg',
            details={
                'network': request.network,
                'social_user': data.user,
                'social_login': data.login,
            },
        )

        user = User(
            login=data.login or None,
            name=data.name or None,
            surname=data.surname or None,
            social=[{
                'id': request.network, # TODO: Several accounts in one network
                'user': data.user,
                'login': data.login,
                'name': data.name,
                'surname': data.surname,
                'language': request.locale,
            }],
            actions=[action.json(default=False)], # TODO: without `.json()`
            # TODO: avatar
        )

        user.save()

        # Report
        await report.important(
            "User registration by bot",
            {
                'user': user.id,
                'name': f"{data.name or ''} {data.surname or ''}",
                'login': data.login and f"@{data.login}",
                'token': request.token,
                'network': request.network,
            },
            tags=['reg'],
        )

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('auth')

    try:
        token = Token.get(ids=request.token, fields={'user'})
    except:
        token = Token(id=request.token)

    if token.user:
        await report.warning(
            "Reauth",
            {'from': token.user, 'to': user.id, 'token': request.token},
        )

    token.user = user.id
    token.save()

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }
