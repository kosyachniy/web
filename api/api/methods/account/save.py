"""
The editing method of the account object of the API
"""

from typing import Union
from copy import deepcopy

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.user import User
from api.models.action import Action


class Type(BaseType):
    login: str = None
    password: str = None
    avatar: str = None
    name: str = None
    surname: str = None
    phone: str = None
    mail: str = None
    social: list[dict] = None
    description: str = None
    language: Union[str, int] = None
    mailing: dict = None

@validate(Type)
async def handle(request, data):
    """ Save personal information """

    # No access
    if request.user.status < 3:
        raise ErrorAccess('edit')

    # Get
    user = User.get(ids=request.user.id)

    # Change fields
    # TODO: Fix exceptions on bad fields

    user.login = data.login
    user.password = data.password
    user.avatar = data.avatar
    user.name = data.name
    user.surname = data.surname

    phone_old = deepcopy(user.phone)
    user.phone = data.phone
    if phone_old != user.phone:
        user.phone_verified = False

    user.mail = data.mail
    user.social = data.social # TODO: checking
    user.description = data.description
    user.language = data.language

    user.mailing = data.mailing

    # Action tracking
    action = Action(
        title='acc_save',
    )
    user.actions.append(action.json(default=False))

    # Save
    user.save()

    # Processing
    ## Avatar
    avatar = None
    if data.avatar != user.avatar:
        avatar = user.avatar

    ## Phone
    phone = None
    if phone_old != user.phone:
        phone = user.phone

    # Response
    return {
        'avatar':  avatar,
        'phone':  phone,
    }
