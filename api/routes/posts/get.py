"""
The getting method of the post object of the API
"""

import re
from typing import Union

from fastapi import APIRouter, Body, Depends # Request
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.post import Post
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: Union[int, list[int]] = None
    limit: int = None
    offset: int = None
    search: str = None
    my: bool = None
    # TODO: category: int = None
    # TODO: locale: str = None
    # TODO: fields: list[str] = None

@router.post("/get/")
async def handler(
    # request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Get """

    # TODO: data.my for unauth
    # TODO: access only to your posts

    # No access
    # TODO: -> middleware
    if user.status < 2:
        raise ErrorAccess('get')

    # # Language
    # # TODO: pre-processing params (None, strip(), value -> code)
    # if data.locale:
    #     data.locale = data.locale # TODO: case if None
    # else:
    #     data.locale = request.state.locale

    # Fields
    fields = {
        'id',
        'title',
        'data',
        'reactions',
        'image',
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

    cond_user = None
    if data.my:
        cond_user = user.id
    elif data.my is not None:
        cond_user = {'$ne': user.id}

    posts = Post.complex(
        ids=data.id,
        user=cond_user,
        limit=data.limit,
        offset=data.offset,
        search=data.search,
        fields=fields,  # None if data.id else fields,
        # category=data.category,
        # locale=data.locale,
        handler=handle,
    )

    # Sort
    if isinstance(posts, list):
        posts = sorted(posts, key=lambda x: x['updated'], reverse=True)

    # Response
    return {
        'posts': posts,
    }
