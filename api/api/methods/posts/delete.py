"""
The removal method of the post object of the API
"""

from consys.errors import ErrorAccess

from api.lib import BaseType, validate
from api.models.post import Post


class Type(BaseType):
    id: int

@validate(Type)
async def handle(request, data):
    """ Delete """

    # No access
    if request.user.status < 7:
        raise ErrorAccess('delete')

    # Get
    post = Post.get(ids=data.id)

    # Delete
    post.rm()
