"""
The getting method of the review object of the API
"""

from ...funcs import check_params
from ...funcs.mongodb import db
from ...models.user import User
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

    reviews = list(db.reviews.find(
        {},
        {'_id': False}
    ).sort('time', -1)[0:count])

    for review in reviews:
        review['user'] = User.get(ids=review['user'], fields={
            'login',
            'name',
            'surname',
            'avatar',
        })

    # Response

    res = {
        'reviews': reviews,
    }

    return res
