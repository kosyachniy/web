"""
The removal method of the review object of the API
"""

from ...funcs import check_params
from ...funcs.mongodb import db
from ...errors import ErrorAccess


async def handle(this, **x):
    """ Delete """

    # Checking parameters
    check_params(x, (
        ('id', True, int),
    ))

    # No access
    if this.user['status'] < 5:
        raise ErrorAccess('token')

    # Get feedback

    feedback = db['feedback'].find_one({'id': x['id']}, {'_id': True})

    ## Wrong ID
    if not feedback:
        raise ErrorWrong('id')

    # Remove feedback
    db['feedback'].remove(feedback['_id'])
