from fastapi import routing

from .cancel import router as cancel_router
from .create import router as create_router


router = routing.APIRouter(prefix="/payments")
router.include_router(cancel_router)
router.include_router(create_router)
