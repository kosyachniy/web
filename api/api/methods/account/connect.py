"""
The connect socket of the account object of the API
"""

# pylint: disable=unused-argument
async def handle(this, request):
    """ Connect """

    print('IN', this.socket)
