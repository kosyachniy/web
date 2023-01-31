"""
Attach all routers
"""

import importlib
import pkgutil

# pylint: disable=import-self
import routes
from app import app


for loader, module_name, is_pkg in pkgutil.walk_packages(
    routes.__path__, routes.__name__ + '.'
):
    try:
        names = module_name.split('.')[1:-1]
        if not names:
            continue

        module = importlib.import_module(module_name)
        if not hasattr(module, 'router'):
            continue
        # pylint: disable=invalid-name
        name = '/' + '/'.join(names)
        app.include_router(module.router, prefix=name, tags=names)

    except Exception as e:  # pylint: disable=broad-except
        print(e)
