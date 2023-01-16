"""
The getting method of the review object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.user import User
from models.review import Review
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int | list[int] = None
    limit: int = None
    offset: int = None
    search: str = None
    # TODO: fields: list[str] = None

@router.post("/get/")
async def handler(
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Get """

    # TODO: get by your token when you unauth

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
            review['user'] = User.complex(review['user'], fields={
                'id',
                'login',
                'name',
                'surname',
                'image',
            })

        return review

    # Get
    reviews = Review.complex(
        ids=data.id,
        limit=data.limit,
        offset=data.offset,
        search=data.search,
        fields=fields,
        handler=handle,
    )

    # Response
    return {
        'reviews': reviews,
    }
