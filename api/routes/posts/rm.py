"""
The removal method of the post object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess, ErrorWrong

from models.post import Post
from services.auth import auth


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/rm/")
async def handler(
    data: Type = Body(...),
    user = Depends(auth),
):
    """ Delete """

    # No access
    if user.status < 3:
        raise ErrorAccess('rm')

    # Get
    try:
        post = Post.get(
            ids=data.id,
            user=(user.id or None) if user.status < 7 else None,
        )
    except ErrorWrong as e:
        raise ErrorAccess('rm') from e

    # Delete
    post.rm()
