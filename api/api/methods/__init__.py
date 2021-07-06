"""
Import API methods from submodules and call the API method
"""

from pathlib import Path
import importlib
import importlib.util
# import pkgutil

from ..errors import ErrorWrong


CURRENT_PATH = str(Path(__file__).parent) + '/'
CURRENT_MODULE = CURRENT_PATH.replace('/', '.')


async def call(method, this, params):
    """ Call the API method """

    module_name = CURRENT_MODULE + method
    module_spec = importlib.util.find_spec(module_name)

    if module_spec is None:
        raise ErrorWrong('method')

    module = importlib.import_module(module_name)
    handle = getattr(module, 'handle')
    return await handle(this, params)


# for loader, module_name, is_pkg in pkgutil.walk_packages(
#     [CURRENT_PATH], CURRENT_MODULE,
# ):
#     print(importlib.import_module(module_name))
