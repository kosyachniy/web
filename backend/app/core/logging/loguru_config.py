"""
Loguru Logging Configuration

Advanced structured logging setup with JSON formatting, correlation ID tracking,
and integration with FastAPI request lifecycle.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from loguru import logger

from app.core.config import Settings


async def setup_logging(settings: Settings) -> None:
    """
    Configure loguru with structured JSON logging and proper formatting.

    Args:
        settings: Application settings containing logging configuration
    """
    # Remove default loguru handler
    logger.remove()

    # Configure log format based on environment
    log_format = _get_log_format(settings)

    # Console logging
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.log_level.value,
        serialize=settings.log_format == "json",
        colorize=settings.log_format != "json" and settings.is_development,
        backtrace=settings.debug,
        diagnose=settings.debug,
        enqueue=True,  # Async logging
        catch=True,    # Catch exceptions in logged functions
    )

    # File logging (if configured)
    if settings.log_file:
        log_file_path = Path(settings.log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Regular log file
        logger.add(
            str(log_file_path),
            format=log_format,
            level=settings.log_level.value,
            serialize=True,  # Always JSON for file logs
            rotation="100 MB",
            retention="30 days",
            compression="gz",
            backtrace=settings.debug,
            diagnose=settings.debug,
            enqueue=True,
            catch=True,
        )

        # Error-only log file
        error_log_path = log_file_path.with_suffix(".error.log")
        logger.add(
            str(error_log_path),
            format=log_format,
            level="ERROR",
            serialize=True,
            rotation="50 MB",
            retention="90 days",
            compression="gz",
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
        )

    # Configure specific loggers
    _configure_external_loggers(settings)

    # Add request correlation context
    _setup_correlation_context()

    logger.info(
        "Logging configured",
        level=settings.log_level.value,
        format=settings.log_format,
        file_logging=settings.log_file is not None,
    )


def _get_log_format(settings: Settings) -> str:
    """Get log format string based on configuration."""
    if settings.log_format == "json":
        # JSON format for structured logging
        return (
            "{"
            '"timestamp": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
            '"level": "{level}", '
            '"logger": "{name}", '
            '"module": "{module}", '
            '"function": "{function}", '
            '"line": {line}, '
            '"correlation_id": "{extra[correlation_id]}", '
            '"request_id": "{extra[request_id]}", '
            '"user_id": "{extra[user_id]}", '
            '"message": "{message}", '
            '"extra": {extra}'
            "}"
        )
    else:
        # Human-readable format for development
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<yellow>{extra[correlation_id]}</yellow> | "
            "<level>{message}</level> "
            "{extra}"
        )


def _configure_external_loggers(settings: Settings) -> None:
    """Configure external library loggers."""
    import logging

    # Intercept standard library logging
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Replace handler for specific loggers
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("fastapi").handlers = [InterceptHandler()]

    # Set levels for external loggers
    logging.getLogger("sqlalchemy.engine").setLevel(
        getattr(logging, settings.monitoring.database_log_level)
    )
    logging.getLogger("httpx").setLevel(
        getattr(logging, settings.monitoring.http_client_log_level)
    )
    logging.getLogger("celery").setLevel(logging.WARNING)
    logging.getLogger("aio_pika").setLevel(logging.WARNING)


def _setup_correlation_context() -> None:
    """Setup correlation ID context for all log messages."""
    from .correlation import get_correlation_id, get_request_id, get_user_id

    # Configure default extra values
    logger.configure(
        extra={
            "correlation_id": lambda: get_correlation_id() or "no-correlation-id",
            "request_id": lambda: get_request_id() or "no-request-id",
            "user_id": lambda: get_user_id() or "anonymous",
        }
    )


def get_logger(name: str) -> Any:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logger.bind(name=name)


def log_function_call(func_name: str, **kwargs: Any) -> None:
    """Log function call with parameters."""
    logger.debug(
        f"Function called: {func_name}",
        function=func_name,
        parameters=kwargs,
    )


def log_performance(operation: str, duration: float, **metadata: Any) -> None:
    """Log performance metrics."""
    logger.info(
        f"Performance: {operation}",
        operation=operation,
        duration_seconds=duration,
        **metadata,
    )


def log_security_event(event_type: str, **details: Any) -> None:
    """Log security-related events."""
    logger.warning(
        f"Security event: {event_type}",
        event_type=event_type,
        security=True,
        **details,
    )


def log_business_event(event_type: str, **details: Any) -> None:
    """Log business-related events for analytics."""
    logger.info(
        f"Business event: {event_type}",
        event_type=event_type,
        business=True,
        **details,
    )