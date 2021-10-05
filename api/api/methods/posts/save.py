"""
The creating and editing method of the post object of the API
"""

from consys.errors import ErrorAccess

from ...lib import BaseType, validate
from ...lib.reports import report
from ...models.post import Post


class Type(BaseType):
    id: int = None
    name: str = None
    cont: str = None
    cover: str = None
    tags: list[str] = None
    # category: int = None

@validate(Type)
async def handle(this, request, data):
    """ Save """

    # No access
    if request.user.status < 2:
        raise ErrorAccess('save')

    # Get

    new = False

    if data.id:
        post = Post.get(ids=data.id, fields={})
    else:
        post = Post(
            user=request.user.id,
        )
        new = True

    # Change fields
    post.name = data.name # TODO: checking if add
    post.tags = data.tags
    post.cont = data.cont # TODO: checking if add
    post.cover = data.cover
    # TODO: category

    # Save
    post.save()

    # Report
    await report.important(
        "Save post",
        {
            'review': post.id,
            'name': post.name,
            'user': request.user.id,
            'new': new,
        },
    )

    # Processing
    cont = None
    if data.cont and data.cont != post.cont:
        cont = post.cont

    # Response
    return {
        'id': post.id,
        'cont': cont,
        'new': new,
    }
