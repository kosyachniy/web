"""
Global error handling and custom exception definitions.
Implements RFC 7807 Problem Details for HTTP APIs.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .logging import get_logger

logger = get_logger(__name__)


class APIError(Exception):
    """Base API error with support for RFC 7807 Problem Details."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        instance: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.instance = instance
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to RFC 7807 Problem Details format."""
        problem = {
            "type": f"/errors/{self.error_code.lower()}",
            "title": self.__class__.__name__.replace("Error", ""),
            "status": self.status_code,
            "detail": self.message,
        }

        if self.instance:
            problem["instance"] = self.instance

        if self.details:
            problem.update(self.details)

        return problem


class ValidationError(APIError):
    """Validation error for request data."""

    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="ValidationError",
            **kwargs
        )
        if field:
            self.details["field"] = field


class AuthenticationError(APIError):
    """Authentication failed error."""

    def __init__(self, message: str = "Authentication required", **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AuthenticationError",
            **kwargs
        )


class AuthorizationError(APIError):
    """Authorization/permission denied error."""

    def __init__(self, message: str = "Access denied", **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AuthorizationError",
            **kwargs
        )


class NotFoundError(APIError):
    """Resource not found error."""

    def __init__(self, message: str = "Resource not found", resource: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NotFoundError",
            **kwargs
        )
        if resource:
            self.details["resource"] = resource


class ConflictError(APIError):
    """Resource conflict error."""

    def __init__(self, message: str = "Resource conflict", **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="ConflictError",
            **kwargs
        )


class RateLimitError(APIError):
    """Rate limit exceeded error."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RateLimitError",
            **kwargs
        )
        if retry_after:
            self.details["retry_after"] = retry_after


class ServiceUnavailableError(APIError):
    """Service unavailable error."""

    def __init__(self, message: str = "Service temporarily unavailable", **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="ServiceUnavailableError",
            **kwargs
        )


class BusinessLogicError(APIError):
    """Business logic validation error."""

    def __init__(self, message: str, rule: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="BusinessLogicError",
            **kwargs
        )
        if rule:
            self.details["rule"] = rule


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle custom API errors."""
    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "API error occurred",
        extra={
            "error_type": exc.__class__.__name__,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "message": exc.message,
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
            "details": exc.details
        }
    )

    problem_details = exc.to_dict()
    problem_details["instance"] = exc.instance or request.url.path

    return JSONResponse(
        status_code=exc.status_code,
        content=problem_details,
        headers={"Content-Type": "application/problem+json"}
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "HTTP exception occurred",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
        }
    )

    problem_details = {
        "type": f"/errors/http_{exc.status_code}",
        "title": "HTTP Error",
        "status": exc.status_code,
        "detail": exc.detail,
        "instance": request.url.path,
    }

    return JSONResponse(
        status_code=exc.status_code,
        content=problem_details,
        headers={"Content-Type": "application/problem+json"}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")

    # Format validation errors
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    logger.warning(
        "Validation error occurred",
        extra={
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
            "errors": errors,
        }
    )

    problem_details = {
        "type": "/errors/validation_error",
        "title": "Validation Error",
        "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "detail": "Request validation failed",
        "instance": request.url.path,
        "errors": errors,
    }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=problem_details,
        headers={"Content-Type": "application/problem+json"}
    )


async def internal_server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected internal server errors."""
    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "Internal server error occurred",
        extra={
            "error_type": exc.__class__.__name__,
            "error_message": str(exc),
            "request_id": request_id,
            "path": request.url.path,
            "method": request.method,
        },
        exc_info=True
    )

    problem_details = {
        "type": "/errors/internal_server_error",
        "title": "Internal Server Error",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "detail": "An unexpected error occurred",
        "instance": request.url.path,
    }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=problem_details,
        headers={"Content-Type": "application/problem+json"}
    )