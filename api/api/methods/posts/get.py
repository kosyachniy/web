"""
The getting method of the post object of the API
"""

import re
from typing import Union

from ...funcs import BaseType, validate
from ...models.post import Post
from ...errors import ErrorAccess


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    search: str = None
    # TODO: category: int = None
    # TODO: language: Union[str, int] = None
    # TODO: fields: list[str] = None

# pylint: disable=unused-argument
@validate(Type)
async def handle(this, request, data):
    """ Get """

    # No access
    if request.user.status < 2:
        raise ErrorAccess('get')

    # # Language
    # # TODO: pre-processing params (None, strip(), value -> code)
    # if data.language:
    #     data.language = get_language(data.language)
    # else:
    #     data.language = request.language

    # Fields
    fields = {
        'name',
        'cont',
        'reactions',
        'cover',
        'created',
        # 'geo',
    }

    # Get
    posts = Post.get(
        ids=data.id,
        count=data.count,
        offset=data.offset,
        search=data.search,
        fields=fields,
        # category=data.category,
        # language=data.language,
    )

    # Processing
    if isinstance(posts, list):
        for post in posts:
            ## Cover from the first image
            if not post.cover:
                res = re.search(
                    r'<img src="[^"]*">',
                    post.cont
                )

                if res is not None:
                    post.cover = res[0].split('"')[1].split('/')[-1]

            ## Content
            post.cont = re.sub(
                '<[^>]*>',
                '',
                post.cont
            ).replace('&nbsp;', ' ')

    # Response
    return {
        'posts': posts,
    }
