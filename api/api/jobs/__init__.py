"""
Background processes
"""

import asyncio
from pathlib import Path
import pkgutil
import importlib

from api.lib import report


current_path = str(Path(__file__).parent) + '/'
current_module = current_path.replace('/', '.')


async def background(sio):
    """ Background infinite process """

    # Report about start
    await report.info("Restart server")

    # Processes

    handlers = []

    for _, module_name, _ in pkgutil.walk_packages(
        [current_path], current_module,
    ):
        name = module_name.split('.')[-1]
        module = importlib.import_module(module_name[1:])
        handlers.append(getattr(module, name)(sio))

    await asyncio.gather(*handlers)
