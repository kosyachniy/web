"""
The removal method of the post object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from models.track import Track
from services.auth import get_token, auth


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/rm/")
async def handler(
    data: Type = Body(...),
    token = Depends(get_token),
    user = Depends(auth),
):
    """ Delete """

    # No access
    if user.status < 2:
        raise ErrorAccess('rm')

    # Get
    post = Post.get(data.id)

    if (
        user.status < 7
        and (not post.user or post.user != user.id)
        and post.token != token
    ):
        raise ErrorAccess('rm')

    # Delete
    post.rm()

    # Track
    Track(
        title='post_rm',
        data={
            'id': data.id,
        },
        user=user.id,
        token=token,
    ).save()
