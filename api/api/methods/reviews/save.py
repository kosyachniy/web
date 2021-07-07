"""
The creating and editing method of the review object of the API
"""

from ...funcs import BaseType, validate, report
from ...models.review import Review


class Type(BaseType):
    id: int = None
    name: str = None
    cont: str = None

@validate(Type)
async def handle(this, request):
    """ Save """

    # Get

    new = False

    if request.id:
        review = Review.get(ids=request.id, fields={})
    else:
        review = Review(
            user=this.user.id,
        )
        new = True

    # Change fields
    review.name = request.name # TODO: checking if add
    review.cont = request.cont # TODO: checking if add

    # Save
    review.save()

    # Report
    report.request(
        "New review",
        {
            'review': review.id,
            'name': review.name,
            'cont': review.cont,
            'user': this.user.id,
            'token': this.token,
        },
        path='methods.reviews.save',
    )

    # Processing
    cont = None
    if request.cont and request.cont != review.cont:
        cont = review.cont

    # Response
    return {
        'id': review.id,
        'cont': cont,
        'new': new,
    }
