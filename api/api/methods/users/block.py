"""
The blocking method of the user object of the API
"""

from ...funcs import BaseType, validate
from ...models.user import User
from ...errors import ErrorWrong, ErrorAccess


class Type(BaseType):
    id: int

@validate(Type)
async def handle(this, request):
    """ Block """

    # Get user
    try:
        user = User.get(ids=request.id, fields={'status'})
    except:
        raise ErrorWrong('id')

    # No access
    if this.user.status < 6 or user.status > this.user.status:
        raise ErrorAccess('block')

    # Save
    user.status = 1
    user.save()

    # Response
    return {
        'status': user.status,
    }
