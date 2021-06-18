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

    # Single / multiple

    process_single = False

    if 'id' in x and not isinstance(x['id'], (list, tuple, set)):
        process_single = True

    # Fields

    fields = {
        'name',
        'reactions',
        'created',
        # 'geo',
    }

    if process_single:
        fields.add('cont')

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
        if not process_single:
            post.cont = re.sub(
                '<[^>]*>',
                '',
                post.cont
            ).replace('&nbsp;', ' ')

    # Response

    res = {
        'posts': posts,
    }

    return res
