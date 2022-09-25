"""
The creating and editing method of the post object of the API
"""

from consys.errors import ErrorAccess

from api.lib import BaseType, validate, report
from api.models.post import Post


class Type(BaseType):
    id: int = None
    title: str = None
    data: str = None
    image: str = None
    tags: list[str] = None
    # category: int = None

@validate(Type)
async def handle(request, data):
    """ Save """

    # TODO: for unauth by token

    # No access
    if request.user.status < 2:
        raise ErrorAccess('save')

    # Get
    new = False
    if data.id:
        post = Post.get(ids=data.id, user=request.user.id)
    else:
        post = Post(
            user=request.user.id,
        )
        new = True

    # Change fields
    post.title = data.title # TODO: checking if add
    post.tags = data.tags
    post.data = data.data # TODO: checking if add
    post.image = data.image
    # TODO: category

    # Save
    post.save()

    # Report
    if new:
        await report.important("Save post", {
            'post': post.id,
            'title': post.title,
            'user': request.user.id,
        })

    # Response
    return {
        'id': post.id,
        'new': new,
        'post': post.json(),
    }
