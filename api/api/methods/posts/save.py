"""
The creating and editing method of the post object of the API
"""

from ...funcs import BaseType, validate, report
from ...models.post import Post
from ...errors import ErrorAccess


class Type(BaseType):
    id: int = None
    name: str = None
    cont: str = None
    cover: str = None
    tags: list[str] = None
    # category: int = None

@validate(Type)
async def handle(this, request):
    """ Save """

    # No access
    if this.user.status < 2:
        raise ErrorAccess('save')

    # Get

    new = False

    if request.id:
        post = Post.get(ids=request.id, fields={})
    else:
        post = Post(
            user=this.user.id,
        )
        new = True

    # Change fields
    post.name = request.name # TODO: checking if add
    post.tags = request.tags
    post.cont = request.cont # TODO: checking if add
    post.cover = request.cover
    # TODO: category

    # Save
    post.save()

    # Report
    report.important(
        "Save post",
        {
            'review': post.id,
            'name': post.name,
            'user': this.user.id,
            'new': new,
        },
    )

    # Processing
    cont = None
    if request.cont and request.cont != post.cont:
        cont = post.cont

    # Response
    return {
        'id': post.id,
        'cont': cont,
        'new': new,
    }
