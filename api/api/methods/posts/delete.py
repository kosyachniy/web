"""
The removal method of the post object of the API
"""

from ...funcs import check_params
from ...funcs.mongodb import db
from ...errors import ErrorWrong


async def delete(this, **x):
    """ Delete """

    # Checking parameters

    check_params(x, (
        ('id', True, int),
    ))

    # Get

    post = db['posts'].find_one({'id': x['id']})

    ## Wrong ID
    if not post:
        raise ErrorWrong('id')

    # Delete

    db['posts'].remove(post)
