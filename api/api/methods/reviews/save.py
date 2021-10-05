"""
The creating and editing method of the review object of the API
"""

from ...lib import BaseType, validate
from ...lib.reports import report
from ...models.review import Review


class Type(BaseType):
    id: int = None
    name: str = None
    cont: str = None

@validate(Type)
async def handle(this, request, data):
    """ Save """

    # Get

    new = False

    if data.id:
        review = Review.get(ids=data.id, fields={})
    else:
        review = Review(
            user=request.user.id,
        )
        new = True

    # Change fields
    review.name = data.name # TODO: checking if add
    review.cont = data.cont # TODO: checking if add

    # Save
    review.save()

    # Report
    await report.request(
        "New review",
        {
            'review': review.id,
            'name': review.name,
            'cont': review.cont,
            'user': request.user.id,
            'token': request.token,
        },
    )

    # Processing
    cont = None
    if data.cont and data.cont != review.cont:
        cont = review.cont

    # Response
    return {
        'id': review.id,
        'cont': cont,
        'new': new,
    }
