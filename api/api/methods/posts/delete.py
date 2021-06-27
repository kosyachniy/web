"""
The removal method of the post object of the API
"""

from ...funcs import check_params
from ...models.post import Post
from ...errors import ErrorAccess


async def handle(this, **x):
    """ Delete """

    # Checking parameters
    check_params(x, (
        ('id', True, int),
    ))

    # No access
    if this.user.status < 7:
        raise ErrorAccess('delete')

    # Get
    post = Post.get(ids=x['id'])

    # Delete
    post.rm()
