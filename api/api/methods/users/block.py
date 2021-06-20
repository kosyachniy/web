"""
The blocking method of the user object of the API
"""

from ...funcs import check_params
from ...funcs.mongodb import db
from ...errors import ErrorWrong, ErrorAccess


async def handle(this, **x):
    """ Block """

    # Checking parameters

    check_params(x, (
        ('id', True, int),
    ))

    # Get user

    users = db.users.find_one({'id': x['id']})

    ## Wrond ID
    if not users:
        raise ErrorWrong('id')

    # No access
    if this.user['status'] < 6 or users['status'] > this.user['status']:
        raise ErrorAccess('block')

    # Change status
    users['status'] = 1

    # Save
    db.users.save(users)
