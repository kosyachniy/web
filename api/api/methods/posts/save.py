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
    cover: str = None
    tags: list[str] = None
    # category: int = None

@validate(Type)
async def handle(request, data):
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
    post.title = data.title # TODO: checking if add
    post.tags = data.tags
    post.data = data.data # TODO: checking if add
    post.cover = data.cover
    # TODO: category

    # Save
    post.save()

    # Report
    await report.important(
        "Save post",
        {
            'post': post.id,
            'title': post.title,
            'user': request.user.id,
            'new': new,
        },
    )

    # Processing
    cont = None
    if data.data and data.data != post.data:
        cont = post.data

    # Response
    return {
        'id': post.id,
        'data': cont,
        'new': new,
    }
