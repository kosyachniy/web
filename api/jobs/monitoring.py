"""
Monitoring
"""

import asyncio
import subprocess

from prometheus_client import Gauge

from models.user import User
from models.post import Post
from lib import report


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

    except ValueError:
        return None

async def monitoring():
    """ Monitoring """
    metric_posts.set(Post.count())
    metric_users.set(User.count())

async def handle(_):
    """ Monitoring """

    cpu = get_cpu()
    if cpu:
        metric_cpu.set(cpu)

    while True:
        try:
            await monitoring()
        except Exception as e:  # pylint: disable=broad-except
            await report.critical(str(e), error=e)

        await asyncio.sleep(15)
