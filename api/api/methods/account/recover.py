"""
The password recover method of the account object of the API
"""

import hashlib

from ...funcs import check_params
from ...funcs.mongodb import db
from ...errors import ErrorWrong


async def handle(this, **x):
    """ Recover password """

    # Checking parameters

    check_params(x, (
        ('login', True, str),
    ))

    # Get user

    users = db['users'].find_one({'login': x['login']})

    if not users:
        raise ErrorWrong('login')

    password = ''.join(random.sample(ALL_SYMBOLS, 15))
    password_crypt = hashlib.md5(bytes(password, 'utf-8')).hexdigest()

    # Send

    # Update password

    users['password'] = password_crypt
    db['users'].save(users)