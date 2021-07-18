"""
The removal method of the post object of the API
"""

from ...funcs import BaseType, validate
from ...models.post import Post
from ...errors import ErrorAccess


class Type(BaseType):
    id: int

@validate(Type)
async def handle(this, request, data):
    """ Delete """

    # No access
    if request.user.status < 7:
        raise ErrorAccess('delete')

    # Get
    post = Post.get(ids=data.id)

    # Delete
    post.rm()
