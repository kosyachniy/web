"""
The getting method of the post object of the API
"""

import re

from fastapi import APIRouter, Body, Depends, Request
from pydantic import BaseModel
from libdev.lang import to_url
from consys.errors import ErrorAccess

from models.post import Post
from models.category import Category
from models.track import Track
from services.auth import sign
from lib.queue import get


router = APIRouter()


class Type(BaseModel):
    id: int | list[int] = None
    limit: int = 12  # 24 ?
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

    # Action tracking
    if data.search:
        Track(
            title='post_search',
            data={'search': data.search},
            user=user.id,
            token=request.state.token,
            ip=request.state.ip,
        ).save()

    # Fields
    fields = {
        'id',
        'title',
        'data',
        'reactions',
        'image',
        'category',
        'locale',
        'created',
        'updated',
        'status',
        # 'geo',
    }

    # Processing

    if isinstance(data.id, int):
        def handle(post):
            # Add category info
            if post.get('category'):
                category_ids = get('category_ids')
                post['category_data'] = category_ids.get(post['category']).json(
                    fields={'id', 'url', 'title'},
                )
                post['category_data']['parents'] = [
                    category_ids[parent].json(fields={'id', 'url', 'title'})
                    for parent in get('category_parents', {}).get(
                        post['category'], []
                    )
                    if parent in category_ids
                ]

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

            # URL
            post['url'] = to_url(post['title']) or ""
            if post['url']:
                post['url'] += "-"
            post['url'] += f"{post['id']}"

            return post

    cond = {}

    # Personal
    if data.my:
        cond['$or'] = [
            {'user': user.id},
            {'token': request.state.token},
        ]
    elif data.my is not None:
        cond['user'] = {'$ne': user.id}
        cond['token'] = {'$ne': request.state.token}

    # Get
    posts = Post.complex(
        ids=data.id,
        limit=data.limit,
        offset=data.offset,
        search=data.search,
        fields=fields,  # TODO: None if data.id else fields,
        status={'$exists': False} if user.status < 5 else None,
        category=data.category and {
            '$in': Category.get_childs(data.category),
        },
        locale=data.locale and {
            '$in': [None, data.locale],
        },  # NOTE: None → all locales
        extra=cond or None,
        handler=handle,
    )

    # Count
    # TODO: with search
    count = None
    if not data.id:
        if data.search:
            more = Post.get(
                limit=1,
                offset=(data.offset or 0) + data.limit,
                search=data.search,
                fields={},
                status={'$exists': False} if user.status < 5 else None,
                category=data.category and {
                    '$in': Category.get_childs(data.category),
                },
                locale=data.locale and {
                    '$in': [None, data.locale],
                },  # NOTE: None → all locales
                extra=cond or None,
            )
            if more:
                count = data.limit + 1

        else:
            count = Post.count(
                status={'$exists': False} if user.status < 5 else None,
                category=data.category and {
                    '$in': Category.get_childs(data.category),
                },
                locale=data.locale and {
                    '$in': [None, data.locale],
                },  # NOTE: None → all locales
                extra=cond or None,
            )

    # Sort
    if isinstance(posts, list):
        posts = sorted(posts, key=lambda x: x['updated'], reverse=True)

    # Response
    return {
        'posts': posts,
        'count': count,
    }
