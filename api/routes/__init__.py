
import importlib
import pkgutil

from fastapi import APIRouter

import routes


router = APIRouter()

for loader, module_name, is_pkg in pkgutil.walk_packages(
    routes.__path__, routes.__name__ + '.'
):
    names = module_name.split('.')[1:-1]
    if not names:
        continue

    try:
        module = importlib.import_module(module_name)
        name = '/' + '/'.join(names)
        router.include_router(module.router, prefix=name, tags=names)
    except:
        pass
