"""
The connect socket of the account object of the API
"""

# pylint: disable=unused-argument
async def handle(this, **x):
    """ Connect """

    print('IN', this.sid)
