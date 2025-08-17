from fastapi import routing

from .get import router as get_router
from .reply import router as reply_router
from .rm import router as rm_router
from .save import router as save_router


router = routing.APIRouter(prefix="/posts")
router.include_router(get_router)
router.include_router(reply_router)
router.include_router(rm_router)
router.include_router(save_router)
