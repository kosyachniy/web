"""
The removal method of the category object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.category import Category
from models.track import Track
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/rm/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Delete """

    # No access
    if user.status < 2:
        raise ErrorAccess('rm')

    # Get
    category = Category.get(data.id)

    if user.status < 6 and category.user != user.id:
        raise ErrorAccess('rm')

    # Delete
    category.rm()

    # Track
    Track(
        title='cat_rm',
        data={
            'id': data.id,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()
