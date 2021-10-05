"""
The connect socket of the account object of the API
"""

from ...lib.reports import report


async def handle(this, request, data):
    """ Connect """

    await report.debug('IN', request.socket)
