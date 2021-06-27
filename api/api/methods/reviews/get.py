"""
The getting method of the review object of the API
"""

from ...funcs import check_params
from ...models.user import User
from ...models.review import Review
from ...errors import ErrorAccess


async def handle(this, **x):
    """ Get """

    # Checking parameters
    check_params(x, (
        ('id', False, (int, list), int),
        ('count', False, int),
        ('offset', False, int),
        ('search', False, str),
    ))

    # No access
    if this.user.status < 4:
        raise ErrorAccess('get')

    # Fields
    fields = {
        'name',
        'cont',
        'user',
        'created',
        'network',
    }

    # Get
    reviews = Review.get(
        ids=x.get('id', None),
        count=x.get('count', None),
        offset=x.get('offset', None),
        search=x.get('search', None),
        fields=fields,
    )

    # Processing

    fields = {
        'id',
        'login',
        'name',
        'surname',
        'avatar',
    }

    if isinstance(reviews, list):
        for i, review in enumerate(reviews):
            ## User info
            reviews[i] = review.json(default=False)

            if review.user:
                user = User.get(ids=review.user, fields=fields)
                reviews[i]['user'] = user.json(default=False, fields=fields)

    else:
        reviews = reviews.json(default=False)

        if 'user' in reviews and reviews['user']:
            user = User.get(ids=reviews['user'], fields=fields)
            reviews['user'] = user.json(default=False, fields=fields)

    # Response
    return {
        'reviews': reviews,
    }
