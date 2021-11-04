"""
Import API methods from submodules and call the API method
"""

from pathlib import Path
import importlib
import importlib.util

from consys.errors import ErrorWrong


CURRENT_PATH = str(Path(__file__).parent) + '/'
CURRENT_MODULE = CURRENT_PATH.replace('/', '.')[1:]


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


async def call(method, request, data):
    """ Call the API method """

    module_name = CURRENT_MODULE + method
    module_spec = importlib.util.find_spec(module_name)

    if module_spec is None:
        raise ErrorWrong('method')

    module = importlib.import_module(module_name)
    handle = getattr(module, 'handle')
    response = await handle(request, data)

    # Delete None values
    _rm_none(response)

    return response
