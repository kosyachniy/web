"""
Send websockets process
"""

import asyncio

from api.lib import report
from api.models.job import Job
from api.models.socket import Socket


async def send_sockets(sio):
    """ Send websockets """

    for job in Job.get()[::-1]:
        if not job.users:
            await sio.emit(job.method, job.data)

        elif isinstance(job.users[0], str):
            for socket in job.users:
                await sio.emit(job.method, job.data, room=socket)

        else:
            for user in job.users:
                for socket in Socket.get(user=user, fields={}):
                    await sio.emit(job.method, job.data, room=socket.id)

        job.rm()

async def handle(sio):
    """ Send websockets handler """

    while True:
        try:
            await send_sockets(sio)
        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)

        await asyncio.sleep(0.1) # TODO: change to adapter between nodes
