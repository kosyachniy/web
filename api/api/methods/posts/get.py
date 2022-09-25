"""
The getting method of the post object of the API
"""

import re
from typing import Union

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.post import Post


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    search: str = None
    my: bool = None
    # TODO: category: int = None
    # TODO: language: Union[str, int] = None
    # TODO: fields: list[str] = None

@validate(Type)
async def handle(request, data):
    """ Get """

    # TODO: data.my for unauth
    # TODO: access only to your posts

    # No access
    # TODO: -> middleware
    if request.user.status < 2:
        raise ErrorAccess('get')

    # # Language
    # # TODO: pre-processing params (None, strip(), value -> code)
    # if data.language:
    #     data.language = get_language(data.language) # TODO: case if None
    # else:
    #     data.language = request.language

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
        def handler(post):
            return post

    else:
        def handler(post):
            # Cover from the first image
            if not post.get('image'):
                res = re.search(
                    r'<img src="[^"]*">',
                    post['data']
                )

                if res is not None:
                    post['image'] = res[0].split('"')[1].split('/')[-1]

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
        cond_user = request.user.id
    elif data.my is not None:
        cond_user = {'$ne': request.user.id}

    posts = Post.complex(
        ids=data.id,
        user=cond_user,
        count=data.count,
        offset=data.offset,
        search=data.search,
        fields=fields,  # None if data.id else fields,
        # category=data.category,
        # language=data.language,
        handler=handler,
    )

    # Sort
    if isinstance(posts, list):
        posts = sorted(posts, key=lambda x: x['updated'], reverse=True)

    # Response
    return {
        'posts': posts,
    }
