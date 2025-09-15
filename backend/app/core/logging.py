"""
Structured logging configuration using loguru.
Provides JSON logging for production and human-readable logs for development.
"""
import sys
import json
from typing import Dict, Any, Optional
from loguru import logger

from .settings import settings


class StructuredLoggingFilter:
    """Filter to add structured logging context."""

    def __init__(self):
        self.context: Dict[str, Any] = {}

    def __call__(self, record):
        # Add context to log record
        record["extra"].update(self.context)
        return True

    def bind(self, **kwargs) -> None:
        """Add context to all subsequent logs."""
        self.context.update(kwargs)

    def unbind(self, *keys) -> None:
        """Remove context keys."""
        for key in keys:
            self.context.pop(key, None)

    def clear(self) -> None:
        """Clear all context."""
        self.context.clear()


def json_formatter(record):
    """Custom JSON formatter for structured logging."""
    log_entry = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["name"],
        "function": record["function"],
        "line": record["line"],
    }

    # Add exception information if present
    if record["exception"]:
        log_entry["exception"] = {
            "type": record["exception"].type.__name__,
            "message": str(record["exception"].value),
            "traceback": record["exception"].traceback,
        }

    # Add extra fields
    log_entry.update(record["extra"])

    return json.dumps(log_entry, default=str, ensure_ascii=False)


def text_formatter(record):
    """Human-readable formatter for development."""
    format_string = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # Add extra context if present
    if record["extra"]:
        context_items = [f"{k}={v}" for k, v in record["extra"].items()]
        format_string += " | Context: " + ", ".join(context_items)

    return format_string


def setup_logging():
    """Configure logging based on environment settings."""
    # Remove default logger
    logger.remove()

    # Choose formatter based on environment
    if settings.log_format == "json" or settings.env == "prod":
        formatter = json_formatter
    else:
        formatter = text_formatter

    # Configure log level
    log_level = settings.log_level.upper()

    # Add console handler
    logger.add(
        sys.stdout,
        format=formatter,
        level=log_level,
        colorize=settings.log_format != "json",
        backtrace=True,
        diagnose=True,
    )

    # Add file handler for production
    if settings.env == "prod":
        logger.add(
            "logs/app.log",
            format=json_formatter,
            level=log_level,
            rotation="100 MB",
            retention="30 days",
            compression="gz",
            backtrace=True,
            diagnose=False,  # Don't include sensitive info in file logs
        )

    # Add error file handler
    logger.add(
        "logs/error.log",
        format=json_formatter,
        level="ERROR",
        rotation="50 MB",
        retention="90 days",
        compression="gz",
        backtrace=True,
        diagnose=True,
        filter=lambda record: record["level"].no >= logger.level("ERROR").no,
    )

    logger.info("Logging configuration completed", extra={
        "log_level": log_level,
        "log_format": settings.log_format,
        "environment": settings.env
    })


def get_logger(name: str = None):
    """Get a logger instance with optional name."""
    if name:
        return logger.bind(logger_name=name)
    return logger


def get_request_logger(request_id: str, user_id: Optional[str] = None, endpoint: Optional[str] = None):
    """Get a logger with request context."""
    context = {"request_id": request_id}
    if user_id:
        context["user_id"] = user_id
    if endpoint:
        context["endpoint"] = endpoint

    return logger.bind(**context)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""

    @property
    def logger(self):
        """Get a logger bound to this class."""
        return logger.bind(class_name=self.__class__.__name__)


# Structured logging filter instance
structured_filter = StructuredLoggingFilter()


def bind_context(**kwargs):
    """Bind context to all subsequent logs in the current execution."""
    structured_filter.bind(**kwargs)


def unbind_context(*keys):
    """Remove context keys from logging."""
    structured_filter.unbind(*keys)


def clear_context():
    """Clear all logging context."""
    structured_filter.clear()


# Set up logging on import
setup_logging()