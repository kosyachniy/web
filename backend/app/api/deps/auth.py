"""
Authentication dependencies for FastAPI endpoints.
Provides current user extraction, permission checking, and auth validation.
"""
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core import (
    decode_token,
    AuthenticationError,
    AuthorizationError,
    InvalidTokenError,
    ExpiredTokenError,
    get_logger
)

logger = get_logger(__name__)

# Security scheme for Swagger UI
security = HTTPBearer()


class CurrentUser:
    """Represents the currently authenticated user."""

    def __init__(self, user_id: str, token_payload: dict):
        self.user_id = user_id
        self.token_payload = token_payload
        self.permissions = token_payload.get("permissions", [])
        self.scopes = token_payload.get("scopes", [])

    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return "admin" in self.permissions or "admin" in self.scopes

    @property
    def is_moderator(self) -> bool:
        """Check if user has moderator privileges."""
        return self.is_admin or "moderator" in self.permissions or "moderator" in self.scopes

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        return permission in self.permissions

    def has_scope(self, scope: str) -> bool:
        """Check if user has specific scope."""
        return scope in self.scopes

    def has_any_permission(self, permissions: List[str]) -> bool:
        """Check if user has any of the specified permissions."""
        return any(perm in self.permissions for perm in permissions)

    def has_all_permissions(self, permissions: List[str]) -> bool:
        """Check if user has all of the specified permissions."""
        return all(perm in self.permissions for perm in permissions)

    def __str__(self):
        return f"CurrentUser(user_id={self.user_id})"


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[CurrentUser]:
    """
    Extract current user from token, but don't require authentication.
    Returns None if no valid token is provided.
    """
    if not credentials:
        return None

    try:
        token_payload = decode_token(credentials.credentials, token_type="access")
        user_id = token_payload.get("sub")

        if not user_id:
            logger.warning("Token missing subject (user_id)")
            return None

        logger.debug("User authenticated from token", extra={"user_id": user_id})
        return CurrentUser(user_id=user_id, token_payload=token_payload)

    except (InvalidTokenError, ExpiredTokenError) as e:
        logger.info(f"Invalid or expired token: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Extract current user from JWT token.
    Raises HTTPException if authentication fails.
    """
    if not credentials:
        logger.warning("No authorization credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token_payload = decode_token(credentials.credentials, token_type="access")
        user_id = token_payload.get("sub")

        if not user_id:
            logger.warning("Token missing subject (user_id)")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.debug("User authenticated successfully", extra={"user_id": user_id})
        return CurrentUser(user_id=user_id, token_payload=token_payload)

    except ExpiredTokenError:
        logger.info("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        logger.warning("Invalid token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error during authentication: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        )


def require_permissions(required_permissions: List[str]):
    """
    Dependency factory that requires specific permissions.

    Usage:
        @app.get("/admin/users")
        async def admin_endpoint(user: CurrentUser = Depends(require_permissions(["admin"]))):
            pass
    """
    async def permission_checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current_user.has_any_permission(required_permissions):
            logger.warning(
                "Permission denied",
                extra={
                    "user_id": current_user.user_id,
                    "required_permissions": required_permissions,
                    "user_permissions": current_user.permissions
                }
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(required_permissions)}"
            )
        return current_user

    return permission_checker


def require_admin():
    """Require admin privileges."""
    return require_permissions(["admin"])


def require_moderator():
    """Require moderator or admin privileges."""
    async def moderator_checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current_user.is_moderator:
            logger.warning(
                "Moderator access denied",
                extra={
                    "user_id": current_user.user_id,
                    "permissions": current_user.permissions
                }
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Moderator privileges required"
            )
        return current_user

    return moderator_checker


def require_self_or_admin(user_id_param: str = "user_id"):
    """
    Require user to be accessing their own resource or be an admin.

    Args:
        user_id_param: Name of the path parameter containing the user ID
    """
    async def self_or_admin_checker(
        request_user_id: str,  # This will be injected by the path parameter
        current_user: CurrentUser = Depends(get_current_user)
    ) -> CurrentUser:
        if current_user.user_id != request_user_id and not current_user.is_admin:
            logger.warning(
                "Access denied: user can only access own resources",
                extra={
                    "current_user_id": current_user.user_id,
                    "requested_user_id": request_user_id,
                    "is_admin": current_user.is_admin
                }
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: insufficient privileges"
            )
        return current_user

    return self_or_admin_checker