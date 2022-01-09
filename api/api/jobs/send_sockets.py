"""
Send websockets process
"""

import asyncio

from api.models.job import Job
from api.models.socket import Socket


async def handle(sio):
    """ Send websockets """

    while True:
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

        await asyncio.sleep(0.1) # TODO: change to adapter between nodes
