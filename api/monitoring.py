"""
Monitoring
"""

import asyncio
import subprocess

from prometheus_client import Gauge

from api.lib import report
from api.models.user import User
from api.models.post import Post


p = Gauge('posts', 'Posts')
u = Gauge('users', 'Users')
f = Gauge('cpu_frequency', 'CPU frequency')
try:
    res = subprocess.run(
        "cat /proc/cpuinfo | grep 'MHz' | awk -F': ' '{print $2}'",
        shell=True,
        check=True,
        executable='/bin/bash',
        stdout=subprocess.PIPE,
    ).stdout.decode('utf-8').strip().split('\n')
    res = sum(map(float, res)) * 1000000
except Exception as e:
    pass
else:
    f.set(res)


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
