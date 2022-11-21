"""
The removal method of the review object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.review import Review
from services.request import get_request


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/rm/")
async def handler(
    data: Type = Body(...),
    request = Depends(get_request),
):
    """ Delete """

    # No access
    if request.user.status < 5:
        raise ErrorAccess('rm')

    # Get
    review = Review.get(ids=data.id)

    # Delete
    review.rm()
