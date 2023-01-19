"""
The getting method of the post object of the API
"""

import re

from fastapi import APIRouter, Body, Depends, Request
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int | list[int] = None
    limit: int = None
    offset: int = None
    search: str = None
    my: bool = None
    category: int = None
    locale: str = None
    # TODO: fields: list[str] = None

@router.post("/get/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Get """

    # No access
    # TODO: -> middleware
    if user.status < 2:
        raise ErrorAccess('get')

    # Fields
    fields = {
        'id',
        'title',
        'data',
        'reactions',
        'image',
        'locale',
        'created',
        'updated',
        # 'geo',
    }

    # Processing

    if isinstance(data.id, int):
        def handle(post):
            return post

    else:
        def handle(post):
            # Cover from the first image
            if not post.get('image'):
                res = re.search(
                    r'<img src="([^"]*)">',
                    post['data']
                )
                if res is not None:
                    post['image'] = res.groups()[0]

            # Content
            post['data'] = re.sub(
                r'<[^>]*>',
                '',
                post['data']
            ).replace('&nbsp;', ' ')

            return post

    # Get

    cond = None
    if data.my:
        cond = {'$or': [{'user': user.id}, {'token': request.state.token}]}
    elif data.my is not None:
        cond = {'user': {'$ne': user.id}, 'token': {'$ne': request.state.token}}

    posts = Post.complex(
        ids=data.id,
        limit=data.limit,
        offset=data.offset,
        search=data.search,
        fields=fields,  # None if data.id else fields,
        category=data.category,  # TODO: or childs
        locale=data.locale,  # NOTE: None → all locales
        extra=cond,
        handler=handle,
    )

    # Sort
    if isinstance(posts, list):
        posts = sorted(posts, key=lambda x: x['updated'], reverse=True)

    # Response
    return {
        'posts': posts,
    }
