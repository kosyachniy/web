"""
The creating and editing method of the review object of the API
"""

from ...funcs import check_params, reimg
from ...models.review import Review


async def handle(this, **x):
    """ Save """

    # Checking parameters
    ## Edit
    if 'id' in x:
        check_params(x, (
            ('id', True, int),
            ('name', False, str),
            ('cont', False, str),
        ))

    ## Add
    else:
        check_params(x, (
            ('name', True, str),
            ('cont', True, str),
        ))

    # Processing params
    processed = False

    # Get
    if 'id' in x:
        review = Review.get(ids=x['id'], fields={})
    else:
        review = Review(
            user=this.user.id,
        )

    # Change fields
    review.name = x['name']

    ## Content
    review.cont = reimg(x['cont'])

    if x['cont'] != review.cont:
        processed = True

    # Save
    review.save()

    # Response
    return {
        'id': review.id,
        'cont': review.cont if processed else None,
    }
