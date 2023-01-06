"""
The getting method of the review object of the API
"""

from typing import Union

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.user import User
from models.review import Review
from services.auth import auth


router = APIRouter()


class Type(BaseModel):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    search: str = None
    # TODO: fields: list[str] = None

@router.post("/get/")
async def handler(
    data: Type = Body(...),
    user = Depends(auth),
):
    """ Get """

    # No access
    if user.status < 4:
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
    def handle(review):
        # User info
        if review.get('user'):
            review['user'] = User.complex(
                ids=review['user'],
                fields={
                    'id',
                    'login',
                    'name',
                    'surname',
                    'image',
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
        handler=handle,
    )

    # Response
    return {
        'reviews': reviews,
    }
