"""
The blocking method of the user object of the API
"""

from ...funcs import BaseType, validate
from ...models.user import User
from ...errors import ErrorWrong, ErrorAccess


class Type(BaseType):
    id: int

@validate(Type)
async def handle(this, request, data):
    """ Block """

    # Get user
    try:
        user = User.get(ids=data.id, fields={'status'})
    except:
        raise ErrorWrong('id')

    # No access
    if request.user.status < 6 or user.status > request.user.status:
        raise ErrorAccess('block')

    # Save
    user.status = 1
    user.save()

    # Response
    return {
        'status': user.status,
    }
