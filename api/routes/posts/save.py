"""
The creating and editing method of the post object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from models.track import Track
from services.auth import sign
from lib import report


router = APIRouter()


class Type(BaseModel):
    id: int = None
    title: str = None
    data: str = None
    image: str = None
    tags: list[str] = None
    # category: int = None

@router.post("/save/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Save """

    # No access
    if user.status < 2:
        raise ErrorAccess('save')

    # Get
    new = False
    if data.id:
        post = Post.get(data.id)

        if (
            user.status < 5
            and (not post.user or post.user != user.id)
            and post.token != request.state.token
        ):
            raise ErrorAccess('save')

    else:
        post = Post(
            user=user.id,
            token=None if user.id else request.state.token,
        )
        new = True

    # Change fields
    post.title = data.title
    post.data = data.data
    post.image = data.image
    post.tags = data.tags
    # TODO: category

    # Save
    post.save()

    # Track
    Track(
        title='post_save',
        data={
            'id': post.id,
            'title': post.title,
            'data': post.data,
            'image': post.image,
            'tags': post.tags,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()

    # Report
    if new:
        await report.important("Save post", {
            'post': post.id,
            'title': post.title,
            'user': user.id,
        })

    # Response
    return {
        'id': post.id,
        'new': new,
        'post': post.json(),
    }
