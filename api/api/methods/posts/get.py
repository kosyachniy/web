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
    # TODO: category: int = None
    # TODO: language: Union[str, int] = None
    # TODO: fields: list[str] = None

@validate(Type)
async def handle(request, data):
    """ Get """

    # No access
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
        'cover',
        'created',
        # 'geo',
    }

    # Processing

    if isinstance(data.id, int):
        def handler(post):
            return post

    else:
        def handler(post):
            # Cover from the first image
            if not post.get('cover'):
                res = re.search(
                    r'<img src="[^"]*">',
                    post['data']
                )

                if res is not None:
                    post['cover'] = res[0].split('"')[1].split('/')[-1]

            # Content
            post['data'] = re.sub(
                r'<[^>]*>',
                '',
                post['data']
            ).replace('&nbsp;', ' ')

            return post

    # Get
    posts = Post.complex(
        ids=data.id,
        count=data.count,
        offset=data.offset,
        search=data.search,
        fields=fields,
        # category=data.category,
        # language=data.language,
        handler=handler,
    )

    # Response
    return {
        'posts': posts,
    }
