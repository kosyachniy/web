from pathlib import Path
import importlib
import importlib.util
# import pkgutil

from ..errors import ErrorWrong


current_path = str(Path(__file__).parent) + '/'
current_module = current_path.replace('/', '.')


async def call(method, this, params):
    """ Call the API method """

    module_name, method_name = method.split('.')
    module_name = current_module + module_name
    module_spec = importlib.util.find_spec(module_name)

    if module_spec is None:
        raise ErrorWrong('method')

    module = importlib.import_module(module_name) # method
    handle = getattr(module, method_name) # 'handle'
    return await handle(this, **params)


# for loader, module_name, is_pkg in pkgutil.walk_packages(
#     [current_path], current_module,
# ):
#     print(importlib.import_module(module_name))
