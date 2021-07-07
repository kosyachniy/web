"""
The removal method of the review object of the API
"""

from ...funcs import BaseType, validate
from ...models.review import Review
from ...errors import ErrorAccess


class Type(BaseType):
    id: int

@validate(Type)
async def handle(this, request):
    """ Delete """

    # No access
    if this.user.status < 5:
        raise ErrorAccess('delete')

    # Get
    review = Review.get(ids=request.id)

    # Delete
    review.rm()
