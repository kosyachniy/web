"""
The creating and editing method of the post object of the API
"""

from ...funcs import check_params, load_image, reimg, report
from ...models.post import Post
from ...errors import ErrorUpload


async def handle(this, **x):
    """ Save """

    # Checking parameters
    ## Edit
    if 'id' in x:
        check_params(x, (
            ('id', True, int),
            ('name', False, str),
            ('cont', False, str),
            ('cover', False, str),
            ('tags', False, list, str),
            # ('category', False, int),
        ))

    ## Add
    else:
        check_params(x, (
            ('name', True, str),
            ('cont', True, str),
            ('cover', False, str),
            ('tags', False, list, str),
            # ('category', False, int),
        ))

    # Processing params
    processed = False
    new = False

    # Get
    if 'id' in x:
        post = Post.get(ids=x['id'], fields={})
    else:
        post = Post(
            user=this.user.id,
        )
        new = True

    # Change fields
    post.name = x['name']
    post.tags = x['tags']
    # TODO: category

    ## Content
    post.cont = reimg(x['cont'])

    if x['cont'] != post.cont:
        processed = True

    ## Cover
    try:
        post.cover = load_image(x['cover'])
    except:
        raise ErrorUpload('cover')

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
        path='methods.posts.save',
    )

    # Response
    return {
        'id': post.id,
        'cont': post.cont if processed else None,
        'new': new,
    }
