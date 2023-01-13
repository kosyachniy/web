"""
The removal method of the review object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.review import Review
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/rm/")
async def handler(
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Delete """

    # No access
    if user.status < 5:
        raise ErrorAccess('rm')

    # Get
    review = Review.get(data.id)

    # Delete
    review.rm()
