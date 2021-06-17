"""
The creating and editing method of the review object of the API
"""

from ...funcs import reimg, check_params, next_id
from ...funcs.mongodb import db


async def handle(this, **x):
    """ Add / edit """

    # Checking parameters

    check_params(x, (
        ('name', True, str),
        ('cont', True, str),
    ))

    #

    query = {
        'id': next_id('feedback'),
        'name': x['name'],
        'cont': reimg(x['cont']),
        'user': this.user['id'],
        'time': this.timestamp,
        'success': 0,
    }

    db['feedback'].insert(query)

    # Response

    res = {
        'id': query['id'],
    }

    return res
