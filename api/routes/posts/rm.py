"""
The removal method of the post object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess, ErrorWrong

from models.post import Post
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
    if request.user.status < 3:
        raise ErrorAccess('rm')

    # Get
    try:
        post = Post.get(
            ids=data.id,
            user=(request.user.id or None) if request.user.status < 7 else None,
        )
    except ErrorWrong as e:
        raise ErrorAccess('rm') from e

    # Delete
    post.rm()
