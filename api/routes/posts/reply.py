"""
Reply method of the post object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from models.comment import Comment
from models.track import Track
from services.auth import sign
from lib import report


router = APIRouter()


class Type(BaseModel):
    post: int
    id: int = None
    data: str = None
    status: int = None

@router.post("/reply/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Save """

    # TODO: fix access to unblock yourself comment

    # No access
    if user.status < 2:
        raise ErrorAccess('save')

    # Check post
    Post.get(data.post, fields={})

    # Get
    new = False
    if data.id:
        comment = Comment.get(data.id)

        if (
            user.status < 5
            and (not comment.user or comment.user != user.id)
            and comment.token != request.state.token
        ):
            raise ErrorAccess('save')

    else:
        comment = Comment(
            user=user.id,
            token=None if user.id else request.state.token,
            post=data.post,
        )
        new = True

    # Change fields
    comment.data = data.data
    comment.status = data.status

    # Save
    comment.save()

    # Track
    Track(
        title='comment_add' if new else 'comment_edit',
        data={
            'id': comment.id,
            'data': comment.data,
            'status': comment.status,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()

    # Report
    if new:
        await report.important("Reply", {
            'post': comment.post,
            'comment': comment.data,
            'user': user.id,
        })

    # Response
    return {
        'id': comment.id,
        'new': new,
        'comment': comment.json(),
    }
