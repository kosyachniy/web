"""
The editing method of the account object of the API
"""

from typing import Union

from ...funcs import BaseType, validate
from ...models.user import User
from ...errors import ErrorAccess


class Type(BaseType):
    login: str = None
    password: str = None
    avatar: str = None
    name: str = None
    surname: str = None
    mail: str = None
    description: str = None
    language: Union[str, int] = None
    social: list[dict] = None

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
    user.mail = request.mail
    user.description = request.description
    user.language = request.language
    user.social = request.social # TODO: checking

    # Save
    user.save()

    # Processing
    avatar = None
    if request.avatar and request.avatar != user.avatar:
        avatar = user.avatar

    # Response
    return {
        'avatar':  avatar,
    }
