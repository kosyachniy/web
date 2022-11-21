"""
The creating and editing method of the post object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from services.request import get_request
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
    request = Depends(get_request),
):
    """ Save """

    # TODO: for unauth by token

    # No access
    if request.user.status < 2:
        raise ErrorAccess('save')

    # Get
    new = False
    if data.id:
        post = Post.get(ids=data.id, user=request.user.id)
    else:
        post = Post(
            user=request.user.id,
        )
        new = True

    # Change fields
    post.title = data.title # TODO: checking if add
    post.tags = data.tags
    post.data = data.data # TODO: checking if add
    post.image = data.image
    # TODO: category

    # Save
    post.save()

    # Report
    if new:
        await report.important("Save post", {
            'post': post.id,
            'title': post.title,
            'user': request.user.id,
        })

    # Response
    return {
        'id': post.id,
        'new': new,
        'post': post.json(),
    }
