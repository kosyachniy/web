"""
The removal method of the post object of the API
"""

from ...funcs import BaseType, validate
from ...models.post import Post
from ...errors import ErrorAccess


class Type(BaseType):
    id: int

@validate(Type)
async def handle(this, request):
    """ Delete """

    # No access
    if this.user.status < 7:
        raise ErrorAccess('delete')

    # Get
    post = Post.get(ids=request.id)

    # Delete
    post.rm()
