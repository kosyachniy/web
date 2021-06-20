"""
The removal method of the review object of the API
"""

from ...funcs import check_params
from ...funcs.mongodb import db
from ...errors import ErrorAccess, ErrorWrong


async def handle(this, **x):
    """ Delete """

    # Checking parameters
    check_params(x, (
        ('id', True, int),
    ))

    # No access
    if this.user['status'] < 5:
        raise ErrorAccess('token')

    # Get

    review = db.reviews.find_one({'id': x['id']}, {'_id': True})

    ## Wrong ID
    if not review:
        raise ErrorWrong('id')

    # Remove
    db.reviews.remove(review['_id'])
