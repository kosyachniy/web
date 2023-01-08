"""
The creating and editing method of the post object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from models.track import Track
from services.auth import get_token, auth
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
    data: Type = Body(...),
    token = Depends(get_token),
    user = Depends(auth),
):
    """ Save """

    # No access
    if user.status < 2:
        raise ErrorAccess('save')

    # Get
    new = False
    if data.id:
        post = Post.get(ids=data.id)

        if (not post.user or post.user != user.id) and post.token != token:
            raise ErrorAccess('save')

    else:
        post = Post(
            user=user.id,
            token=None if user.id else token,
        )
        new = True

    # Change fields
    post.title = data.title # TODO: checking if add
    post.data = data.data # TODO: checking if add
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
        token=token,
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
