from fastapi import routing

# Modern REST endpoints
from .create import router as create_router
from .update import router as update_router
from .delete import router as delete_router
from .list import router as list_router

router = routing.APIRouter(prefix="/categories")

# Include modern REST endpoints
router.include_router(create_router)
router.include_router(update_router)
router.include_router(delete_router)
router.include_router(list_router)
