"""
The removal method of the review object of the API
"""

from ...funcs import BaseType, validate
from ...models.review import Review
from ...errors import ErrorAccess


class Type(BaseType):
    id: int

@validate(Type)
async def handle(this, request, data):
    """ Delete """

    # No access
    if request.user.status < 5:
        raise ErrorAccess('delete')

    # Get
    review = Review.get(ids=data.id)

    # Delete
    review.rm()
