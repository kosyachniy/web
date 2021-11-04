"""
The blocking method of the user object of the API
"""

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.user import User


class Type(BaseType):
    id: int

@validate(Type)
async def handle(request, data):
    """ Block """

    # Get user
    user = User.get(ids=data.id, fields={'status'})

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
