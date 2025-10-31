"""
Correlation ID Context Management

Thread-safe correlation ID, request ID, and user ID tracking for
distributed tracing and request correlation.
"""

from __future__ import annotations

import uuid
from contextvars import ContextVar
from typing import Any

# Context variables for request correlation
_correlation_id: ContextVar[str | None] = ContextVar('correlation_id', default=None)
_request_id: ContextVar[str | None] = ContextVar('request_id', default=None)
_user_id: ContextVar[str | None] = ContextVar('user_id', default=None)
_tenant_id: ContextVar[str | None] = ContextVar('tenant_id', default=None)


def generate_correlation_id() -> str:
    """Generate a new correlation ID."""
    return str(uuid.uuid4())


def generate_request_id() -> str:
    """Generate a new request ID."""
    return str(uuid.uuid4())


def set_correlation_id(correlation_id: str | None) -> str | None:
    """
    Set correlation ID in context.

    Args:
        correlation_id: Correlation ID to set

    Returns:
        Previously set correlation ID
    """
    return _correlation_id.set(correlation_id)


def get_correlation_id() -> str | None:
    """
    Get current correlation ID from context.

    Returns:
        Current correlation ID or None
    """
    return _correlation_id.get()


def get_or_create_correlation_id() -> str:
    """
    Get current correlation ID or create a new one.

    Returns:
        Current or new correlation ID
    """
    correlation_id = get_correlation_id()
    if not correlation_id:
        correlation_id = generate_correlation_id()
        set_correlation_id(correlation_id)
    return correlation_id


def set_request_id(request_id: str | None) -> str | None:
    """
    Set request ID in context.

    Args:
        request_id: Request ID to set

    Returns:
        Previously set request ID
    """
    return _request_id.set(request_id)


def get_request_id() -> str | None:
    """
    Get current request ID from context.

    Returns:
        Current request ID or None
    """
    return _request_id.get()


def get_or_create_request_id() -> str:
    """
    Get current request ID or create a new one.

    Returns:
        Current or new request ID
    """
    request_id = get_request_id()
    if not request_id:
        request_id = generate_request_id()
        set_request_id(request_id)
    return request_id


def set_user_id(user_id: str | None) -> str | None:
    """
    Set user ID in context.

    Args:
        user_id: User ID to set

    Returns:
        Previously set user ID
    """
    return _user_id.set(user_id)


def get_user_id() -> str | None:
    """
    Get current user ID from context.

    Returns:
        Current user ID or None
    """
    return _user_id.get()


def set_tenant_id(tenant_id: str | None) -> str | None:
    """
    Set tenant ID in context for multi-tenancy.

    Args:
        tenant_id: Tenant ID to set

    Returns:
        Previously set tenant ID
    """
    return _tenant_id.set(tenant_id)


def get_tenant_id() -> str | None:
    """
    Get current tenant ID from context.

    Returns:
        Current tenant ID or None
    """
    return _tenant_id.get()


def clear_context() -> None:
    """Clear all context variables."""
    set_correlation_id(None)
    set_request_id(None)
    set_user_id(None)
    set_tenant_id(None)


def get_context_dict() -> dict[str, Any]:
    """
    Get all context variables as a dictionary.

    Returns:
        Dictionary with all context variables
    """
    return {
        'correlation_id': get_correlation_id(),
        'request_id': get_request_id(),
        'user_id': get_user_id(),
        'tenant_id': get_tenant_id(),
    }


def set_context_dict(context: dict[str, Any]) -> None:
    """
    Set context variables from a dictionary.

    Args:
        context: Dictionary with context variables
    """
    if 'correlation_id' in context:
        set_correlation_id(context['correlation_id'])
    if 'request_id' in context:
        set_request_id(context['request_id'])
    if 'user_id' in context:
        set_user_id(context['user_id'])
    if 'tenant_id' in context:
        set_tenant_id(context['tenant_id'])


class ContextManager:
    """Context manager for setting correlation context."""

    def __init__(
        self,
        correlation_id: str | None = None,
        request_id: str | None = None,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ):
        self.correlation_id = correlation_id
        self.request_id = request_id
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.previous_context: dict[str, Any] = {}

    def __enter__(self) -> ContextManager:
        # Save previous context
        self.previous_context = get_context_dict()

        # Set new context
        if self.correlation_id is not None:
            set_correlation_id(self.correlation_id)
        if self.request_id is not None:
            set_request_id(self.request_id)
        if self.user_id is not None:
            set_user_id(self.user_id)
        if self.tenant_id is not None:
            set_tenant_id(self.tenant_id)

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Restore previous context
        set_context_dict(self.previous_context)


def with_correlation_id(correlation_id: str | None = None) -> ContextManager:
    """
    Context manager for setting correlation ID.

    Args:
        correlation_id: Correlation ID to set (generates new if None)

    Returns:
        Context manager
    """
    if correlation_id is None:
        correlation_id = generate_correlation_id()

    return ContextManager(correlation_id=correlation_id)


def with_request_context(
    correlation_id: str | None = None,
    request_id: str | None = None,
    user_id: str | None = None,
    tenant_id: str | None = None,
) -> ContextManager:
    """
    Context manager for setting full request context.

    Args:
        correlation_id: Correlation ID to set
        request_id: Request ID to set
        user_id: User ID to set
        tenant_id: Tenant ID to set

    Returns:
        Context manager
    """
    return ContextManager(
        correlation_id=correlation_id,
        request_id=request_id,
        user_id=user_id,
        tenant_id=tenant_id,
    )