"""
The removal method of the post object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
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
    post = Post.get(data.id)

    # No access
    if (
        user.status < 6
        and (not post.user or post.user != user.id)
        and post.token != request.state.token
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
        token=request.state.token,
        ip=request.state.ip,
    ).save()
