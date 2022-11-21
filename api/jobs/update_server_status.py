"""
Update last server time process
"""

import asyncio
import time

from consys.errors import ErrorWrong

from models.system import System


async def handle(_):
    """ Update last server time """

    while True:
        try:
            system = System.get('last_server_time')
        except ErrorWrong:
            system = System(id='last_server_time')

        system.data = int(time.time())
        system.save()

        await asyncio.sleep(60)
