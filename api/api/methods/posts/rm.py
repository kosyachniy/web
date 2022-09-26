"""
The removal method of the post object of the API
"""

from consys.errors import ErrorAccess, ErrorWrong

from api.lib import BaseType, validate
from api.models.post import Post


class Type(BaseType):
    id: int

@validate(Type)
async def handle(request, data):
    """ Delete """

    # No access
    if request.user.status < 3:
        raise ErrorAccess('rm')

    # Get
    try:
        post = Post.get(
            ids=data.id,
            user=(request.user.id or None) if request.user.status < 7 else None,
        )
    except ErrorWrong as e:
        raise ErrorAccess('rm') from e

    # Delete
    post.rm()
