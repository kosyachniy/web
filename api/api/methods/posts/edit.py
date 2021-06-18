"""
The creating and editing method of the post object of the API
"""

# import re
# import shutil

from ...funcs import reimg, check_params, next_id, load_image
from ...funcs.mongodb import db
from ...errors import ErrorInvalid, ErrorWrong, ErrorUpload


async def handle(this, **x):
    """ Add / edit """

    # Checking parameters

    # Edit
    if 'id' in x:
        check_params(x, (
            ('id', True, int),
            ('name', False, str),
            ('cont', False, str),
            ('cover', False, str),
            ('file', False, str),
            ('category', False, int),
            ('tags', False, list, str),
        ))

    # Add
    else:
        check_params(x, (
            ('name', True, str),
            ('cont', True, str),
            ('cover', False, str),
            ('file', False, str),
            ('category', False, int),
            ('tags', False, list, str),
        ))

    # Processed

    processed = False

    # Formation

    if 'id' in x:
        post = db['posts'].find_one({'id': x['id']})

        # Wrong ID
        if not post:
            raise ErrorWrong('id')

    else:
        post = {
            'id': next_id('posts'),
            'time': this.timestamp,
            'reactions': {
                'likes': [],
                'reposts': [],
                'comments': [],
                'views': [],
            },
        }

    # Change fields
    for field in ('name', 'category', 'tags'):
        if field in x:
            post[field] = x[field]

    ## Content
    if 'cont' in x:
        post_updated = reimg(x['cont'])

        if x['cont'] != post_updated:
            processed = True

        post['cont'] = post_updated

    ## Cover

    if 'cover' in x:
        try:
            file_type = x['file'].split('.')[-1]

        # Invalid file extension
        except:
            raise ErrorInvalid('file')

        try:
            link = load_image(x['cover'], file_type)

        # Error loading cover
        except:
            raise ErrorUpload('cover')

        post['cover'] = link

    ### Cover from the first image
    # try:
    #     img = re.search(
    #         '<img src="[^"]*">',
    #         post['cont']
    #     )[0].split('"')[1].split('/')[2]
    #     shutil.copyfile(
    #         '../data/load/{}'.format(img),
    #         '../data/load/posts/{}.{}'.format(post['id'], img.split('.')[-1])
    #     )
    # except:
    #     pass

    # Save
    db['posts'].save(post)

    # Response

    res = {
        'id': post['id'],
    }

    if processed:
        res['cont'] = post['cont']

    return res
