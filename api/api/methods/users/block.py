"""
The blocking method of the user object of the API
"""

from ...funcs import check_params
from ...models.user import User
from ...errors import ErrorWrong, ErrorAccess


async def handle(this, **x):
    """ Block """

    # Checking parameters
    check_params(x, (
        ('id', True, int),
    ))

    # Get user
    try:
        user = User.get(ids=x['id'], fields={'status'})
    except:
        raise ErrorWrong('id')

    # No access
    if this.user.status < 6 or user.status > this.user.status:
        raise ErrorAccess('block')

    # Save
    user.status = 1
    user.save()
