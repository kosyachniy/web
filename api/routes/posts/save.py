"""
The creating and editing method of the post object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from libdev.lang import to_url
from consys.errors import ErrorAccess

from models.post import Post
from models.track import Track
from services.auth import sign
from lib import report


router = APIRouter()


class Type(BaseModel):
    id: int = None
    title: str = None
    description: str = None
    data: str = None
    image: str = None
    tags: list[str] = None
    locale: str = None
    category: int = None
    status: int = None

@router.post("/save/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Save """

    # TODO: fix access to unblock yourself post

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
    post.description = data.description
    post.data = data.data
    post.image = data.image
    post.tags = data.tags
    post.category = data.category
    post.status = data.status
    if data.locale:
        post.locale = data.locale
    else:
        del post.locale

    # Save
    post.save()

    # Track
    Track(
        title='post_add' if new else 'post_edit',
        data={
            'id': post.id,
            'title': post.title,
            'data': post.data,
            'image': post.image,
            'tags': post.tags,
            'status': post.status,
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
            'locale': post.locale,
            'user': user.id,
        })

    data = post.json()

    # URL
    data['url'] = to_url(post.title) or ""
    if data['url']:
        data['url'] += "-"
    data['url'] += f"{post.id}"

    # Response
    return {
        'id': post.id,
        'new': new,
        'post': data,
    }
