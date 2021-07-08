"""
The editing method of the account object of the API
"""

from typing import Union
from copy import deepcopy

from ...funcs import BaseType, validate
from ...models.user import User
from ...errors import ErrorAccess


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

@validate(Type)
async def handle(this, request):
    """ Save personal information """

    # No access
    if this.user.status < 3:
        raise ErrorAccess('edit')

    # Get
    user = User.get(ids=this.user.id)

    # Change fields

    user.login = request.login
    user.password = request.password
    user.avatar = request.avatar
    user.name = request.name
    user.surname = request.surname

    phone_old = deepcopy(user.phone)
    user.phone = request.phone
    if phone_old != user.phone:
        user.phone_verified = False

    user.mail = request.mail
    user.social = request.social # TODO: checking
    user.description = request.description
    user.language = request.language

    # Save
    user.save()

    # Processing
    ## Avatar
    avatar = None
    if request.avatar != user.avatar:
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
