"""
Monitoring
"""

import asyncio
import subprocess

from prometheus_client import Gauge

from api.lib import report
from api.models.user import User
from api.models.post import Post


metric_posts = Gauge('posts', 'Posts')
metric_users = Gauge('users', 'Users')
metric_cpu = Gauge('cpu_frequency', 'CPU frequency')


def get_cpu():
    """ Get CPU frequency """
    try:
        res = subprocess.run(
            "cat /proc/cpuinfo | grep 'MHz' | awk -F': ' '{print $2}'",
            shell=True,
            check=True,
            executable='/bin/bash',
            stdout=subprocess.PIPE,
        ).stdout.decode('utf-8').strip().split('\n')

        if res == "":
            return None
        return sum(map(float, res)) * 1000000

    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        return None

async def monitoring():
    """ Monitoring """
    metric_posts.set(Post.count())
    metric_users.set(User.count())

async def handle(_):
    """ Monitoring """

    try:
        cpu = get_cpu()
        if cpu:
            metric_cpu.set(cpu)
    except Exception as e:
        await report.critical(str(e), error=e)

    while True:
        try:
            await monitoring()
        # pylint: disable=broad-except
        except Exception as e:
            await report.critical(str(e), error=e)

        await asyncio.sleep(15)
