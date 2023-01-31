"""
Background processes
"""

import asyncio
from pathlib import Path
import pkgutil
import importlib

from lib import report


CURRENT_PATH = str(Path(__file__).parent) + '/'
CURRENT_MODULE = CURRENT_PATH.replace('/', '.')


async def background(sio):
    """ Background infinite process """

    # Report about start
    await report.info("Restart server")

    # Processes

    handlers = []

    for _, module_name, _ in pkgutil.walk_packages(
        [CURRENT_PATH], CURRENT_MODULE,
    ):
        if module_name[0] == '.':
            module_name = module_name[1:]
        if module_name[:4] == 'app.':
            module_name = module_name[4:]
        module = importlib.import_module(module_name)

        if not hasattr(module, 'handle'):
            continue
        count = getattr(module, 'WORKERS', 1)
        for _ in range(count):
            handlers.append(getattr(module, 'handle')(sio))

    if not handlers:
        return

    try:
        await asyncio.gather(*handlers)
    except Exception as e:  # pylint: disable=broad-except
        await report.critical(str(e), error=e)
