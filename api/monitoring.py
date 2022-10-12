"""
Monitoring
"""

import asyncio

from prometheus_client import Gauge

from api.lib import report
from api.models.user import User
from api.models.post import Post


p = Gauge('posts', 'Posts')
u = Gauge('users', 'Users')


async def monitoring():
    """ Monitoring """
    p.set(Post.count())
    u.set(User.count())

async def handlex(_):
    """ Monitoring """

    while True:
        try:
            await monitoring()
        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)

        await asyncio.sleep(15)
