"""
The getting method of the post object of the API
"""

import re
from typing import Union

from ...funcs import BaseType, validate
from ...models.post import Post


class Type(BaseType):
    id: Union[int, list[int]] = None
    count: int = None
    offset: int = None
    search: str = None
    # category: int = None
    # language: Union[str, int] = None
    # fields: list[str] = None

# pylint: disable=unused-argument
@validate(Type)
async def handle(this, request):
    """ Get """

    # # Language
    # # TODO: pre-processing params (None, strip(), value -> code)
    # if request.language:
    #     request.language = get_language(request.language)
    # else:
    #     request.language = this.language

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
        ids=request.id,
        count=request.count,
        offset=request.offset,
        search=request.search,
        fields=fields,
        # category=request.category,
        # language=request.language,
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
