"""
The removal method of the review object of the API
"""

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.review import Review


class Type(BaseType):
    id: int

@validate(Type)
async def handle(request, data):
    """ Delete """

    # No access
    if request.user.status < 5:
        raise ErrorAccess('delete')

    # Get
    review = Review.get(ids=data.id)

    # Delete
    review.rm()
