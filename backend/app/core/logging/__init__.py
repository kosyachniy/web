"""
Logging and Observability Setup

Structured logging configuration with loguru, OpenTelemetry integration,
and correlation ID tracking.
"""

from .loguru_config import setup_logging
from .correlation import get_correlation_id, set_correlation_id

__all__ = ["setup_logging", "get_correlation_id", "set_correlation_id"]