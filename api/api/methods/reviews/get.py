"""
The getting method of the review object of the API
"""

from ...funcs import get_user, check_params
from ...funcs.mongodb import db
from ...errors import ErrorAccess


async def handle(this, **x):
    """ Get """

    # Checking parameters

    check_params(x, (
        ('count', False, int),
    ))

    # No access

    if this.user['status'] < 4:
        raise ErrorAccess('token')

    # Get

    count = x['count'] if 'count' in x else None

    reviews = list(db['reviews'].find(
        {},
        {'_id': False}
    ).sort('time', -1)[0:count])

    for review in reviews:
        review['user'] = get_user(review['user'])

    # Response

    res = {
        'reviews': reviews,
    }

    return res
