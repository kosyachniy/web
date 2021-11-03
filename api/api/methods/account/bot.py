"""
The authorization via social networks method of the account object of the API
"""

from consys.errors import ErrorWrong, ErrorAccess

from ...lib import BaseType, validate, report
from ...models.user import User # process_lower
from ...models.token import Token
from ...models.action import Action
from .auth import reg


class Type(BaseType):
    user: int
    login: str = None
    name: str = None
    surname: str = None

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
        # 'subscription',
        # 'balance',
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
        user = await reg(request, data, 'bot')

    # Assignment of the token to the user

    if not request.token:
        raise ErrorAccess('auth')

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

    # Response
    return {
        **user.json(fields=fields),
        'new': new,
    }
