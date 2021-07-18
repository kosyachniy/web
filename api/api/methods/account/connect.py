"""
The connect socket of the account object of the API
"""

# pylint: disable=unused-argument
async def handle(this, request, data):
    """ Connect """

    print('IN', request.socket)
