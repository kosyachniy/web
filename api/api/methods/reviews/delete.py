"""
The removal method of the review object of the API
"""

from ...funcs import check_params
from ...models.review import Review
from ...errors import ErrorAccess


async def handle(this, **x):
    """ Delete """

    # Checking parameters
    check_params(x, (
        ('id', True, int),
    ))

    # No access
    if this.user.status < 5:
        raise ErrorAccess('delete')

    # Get
    review = Review.get(ids=x['id'])

    # Delete
    review.rm()
