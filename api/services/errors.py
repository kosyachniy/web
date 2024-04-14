from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from lib import log


class ErrorsMiddleware(BaseHTTPMiddleware):
    """Formatting errors middleware"""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:  # pylint: disable=broad-except
            log.exception("An unhandled exception occurred:")
            if isinstance(e, HTTPException):
                return JSONResponse(
                    {"detail": e.detail},
                    status_code=e.status_code,
                )
            return JSONResponse(
                {"detail": "Internal Server Error"},
                status_code=500,
            )

        return response
