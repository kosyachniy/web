"""
The removal method of the post object of the API
"""

from ...funcs import check_params
from ...models.post import Post


# pylint: disable=unused-argument
async def handle(this, **x):
    """ Delete """

    # Checking parameters
    check_params(x, (
        ('id', True, int),
    ))

    # Get
    post = Post.get(ids=x['id'])

    # Delete
    post.rm()
