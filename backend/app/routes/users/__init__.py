from fastapi import routing

from .app import router as app_router
from .auth import router as auth_router
from .block import router as block_router
from .bot import router as bot_router
from .exit import router as exit_router
from .get import router as get_router
from .recover import router as recover_router
from .save import router as save_router
from .social import router as social_router
from .token import router as token_router


router = routing.APIRouter(prefix="/users")
router.include_router(app_router)
router.include_router(auth_router)
router.include_router(block_router)
router.include_router(bot_router)
router.include_router(exit_router)
router.include_router(get_router)
router.include_router(recover_router)
router.include_router(save_router)
router.include_router(social_router)
router.include_router(token_router)
