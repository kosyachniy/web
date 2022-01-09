"""
The getting method of the review object of the API
"""

from typing import Union

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.user import User
from api.models.review import Review


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    search: str = None
    # TODO: fields: list[str] = None

@validate(Type)
async def handle(request, data):
    """ Get """

    # No access
    if request.user.status < 4:
        raise ErrorAccess('get')

    # Fields
    fields = {
        'id',
        'title',
        'data',
        'user',
        'created',
        'network',
    }

    # Processing
    def handler(review):
        # User info
        if review.get('user'):
            review['user'] = User.complex(
                ids=review['user'],
                fields={
                    'id',
                    'login',
                    'name',
                    'surname',
                    'avatar',
                },
                handler=lambda el: el,
            )

        return review

    # Get
    reviews = Review.complex(
        ids=data.id,
        count=data.count,
        offset=data.offset,
        search=data.search,
        fields=fields,
        handler=handler,
    )

    # Response
    return {
        'reviews': reviews,
    }
