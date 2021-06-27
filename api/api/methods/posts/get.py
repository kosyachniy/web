"""
The getting method of the post object of the API
"""

import re

from ...funcs import check_params
from ...models.post import Post


# pylint: disable=unused-argument
async def handle(this, **x):
    """ Get """

    # Checking parameters
    check_params(x, (
        ('id', False, (int, list), int),
        ('count', False, int),
        ('offset', False, int),
        ('search', False, str),
        # ('category', False, int),
        # ('language', False, (int, str)),
    ))

    # # Language
    # # TODO: pre-processing params (None, strip(), value -> code)
    # if 'language' in x:
    #     x['language'] = get_language(x['language'])
    # else:
    #     x['language'] = this.language

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
        ids=x.get('id', None),
        count=x.get('count', None),
        offset=x.get('offset', None),
        search=x.get('search', None),
        fields=fields,
        # category=x.get('category', None),
        # language=x.get('language', None),
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
