"""
The getting method of the post object of the API
"""

import re

from fastapi import APIRouter, Body, Depends, Request
from pydantic import BaseModel
from libdev.lang import get_pure
from consys.errors import ErrorAccess

from models.user import User
from models.post import Post
from models.comment import Comment
from models.category import Category
from models.track import Track
from models.reaction import Reaction
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
    utm: str = None
    # TODO: fields: list[str] = None

# pylint: disable=too-many-statements,too-many-branches
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

    extend = isinstance(data.id, int)

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
        'image',
        'url',
        'created',
        'updated',
        'status',
    }
    if extend:
        fields |= {
            'description',
            'category',
            'locale',
            'user',
        }

    # Processing

    if extend:
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

            # Author
            if post.get('user'):
                post['author'] = User.get(post['user']).json(fields={
                    'id', 'login', 'name', 'surname', 'title', 'image',
                })

            # Comments
            post['comments'] = []
            users = {}
            for comment in Comment.complex(
                post=post['id'],
                status={'$exists': False},
                fields={'id', 'data', 'user', 'created'},
            ):
                if comment.get('user'):
                    if comment['user'] not in users:
                        users[comment['user']] = User.complex(
                            ids=comment['user'],
                            fields={'id', 'name', 'surname', 'title', 'image'},
                        )
                    comment['user'] = users[comment['user']]
                else:
                    del comment['user']
                post['comments'].append(comment)

            # Views counter
            post['views'] = len(Reaction.get(
                type={'$exists': False},
                post=data.id,
            ))

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
            post['data'] = get_pure(post['data']).split('\n')[0]

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
        fields=fields,
        status={'$exists': False} if user.status < 5 else None,
        category={
            '$in': Category.get_childs(data.category),
        } if data.category else None,
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

    # Views counter
    # pylint: disable=too-many-nested-blocks
    if extend and (user.id or request.state.token):
        reactions = Reaction.get(
            type={'$exists': False},
            post=data.id,
            extra={
                '$or': [
                    {'user': user.id},
                    {'token': request.state.token},
                ],
            },
        )
        if reactions:
            if user.id:
                viewed = False
                for reaction in reactions[::-1]:
                    if reaction.user:
                        if reaction.user == user.id:
                            viewed = True
                        continue
                    if viewed:
                        reaction.rm()
                        continue
                    reaction.user = user.id
                    reaction.save()
                    viewed = True
        else:
            Reaction(
               post=data.id,
               user=user.id,
               token=request.state.token,
               utm=data.utm or None,
            ).save()

    # Response
    return {
        'posts': posts,
        'count': count,
    }
