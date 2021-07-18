"""
The getting method of the review object of the API
"""

from typing import Union

from ...funcs import BaseType, validate
from ...models.user import User
from ...models.review import Review
from ...errors import ErrorAccess


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    search: str = None
    # TODO: fields: list[str] = None

@validate(Type)
async def handle(this, request, data):
    """ Get """

    # No access
    if request.user.status < 4:
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
        ids=data.id,
        count=data.count,
        offset=data.offset,
        search=data.search,
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
            reviews[i] = review.json(default=False)

            ## User info
            if review.user:
                user = User.get(ids=review.user, fields=fields)
                reviews[i]['user'] = user.json(default=False, fields=fields)

    else:
        reviews = reviews.json(default=False)

        ## User info
        if 'user' in reviews and reviews['user']:
            user = User.get(ids=reviews['user'], fields=fields)
            reviews['user'] = user.json(default=False, fields=fields)

    # Response
    return {
        'reviews': reviews,
    }
