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


def _rm_none(data):
    """ Remove None values """

    if not isinstance(data, dict):
        return

    for field in set(data):
        if data[field] is None:
            del data[field]
            continue

        if isinstance(data[field], dict):
            _rm_none(data[field])
            continue

        if isinstance(data[field], (list, tuple, set)):
            for el in data[field]:
                _rm_none(el)


async def call(method, this, request, data):
    """ Call the API method """

    module_name = CURRENT_MODULE + method
    module_spec = importlib.util.find_spec(module_name)

    if module_spec is None:
        raise ErrorWrong('method')

    module = importlib.import_module(module_name)
    handle = getattr(module, 'handle')
    response = await handle(this, request, data)

    # Delete None values
    _rm_none(response)

    return response


# for loader, module_name, is_pkg in pkgutil.walk_packages(
#     [CURRENT_PATH], CURRENT_MODULE,
# ):
#     print(importlib.import_module(module_name))
