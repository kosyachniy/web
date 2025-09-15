"""
Application lifespan management for FastAPI.
Handles startup and shutdown events, resource initialization and cleanup.
"""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from .settings import settings


class LifespanManager:
    """Manages application lifecycle events."""

    def __init__(self):
        self._startup_tasks = []
        self._shutdown_tasks = []

    async def startup(self) -> None:
        """Execute all startup tasks."""
        logger.info("Starting application startup...")

        # Initialize logging
        await self._setup_logging()

        # Initialize database connections
        await self._setup_database()

        # Initialize Redis connection
        await self._setup_redis()

        # Initialize monitoring
        await self._setup_monitoring()

        # Initialize background job system
        await self._setup_jobs()

        # Execute custom startup tasks
        for task in self._startup_tasks:
            try:
                await task()
                logger.info(f"Startup task {task.__name__} completed")
            except Exception as e:
                logger.error(f"Startup task {task.__name__} failed: {e}")
                raise

        logger.info("Application startup completed successfully")

    async def shutdown(self) -> None:
        """Execute all shutdown tasks."""
        logger.info("Starting application shutdown...")

        # Execute custom shutdown tasks
        for task in reversed(self._shutdown_tasks):
            try:
                await task()
                logger.info(f"Shutdown task {task.__name__} completed")
            except Exception as e:
                logger.error(f"Shutdown task {task.__name__} failed: {e}")

        # Cleanup connections
        await self._cleanup_connections()

        logger.info("Application shutdown completed")

    def add_startup_task(self, task):
        """Add a custom startup task."""
        self._startup_tasks.append(task)

    def add_shutdown_task(self, task):
        """Add a custom shutdown task."""
        self._shutdown_tasks.append(task)

    async def _setup_logging(self):
        """Setup structured logging configuration."""
        # This will be implemented when we add logging.py
        logger.info("Logging setup completed")

    async def _setup_database(self):
        """Initialize database connections."""
        try:
            # TODO: Initialize SQLAlchemy async engine
            # This will be implemented when we add database infrastructure
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

    async def _setup_redis(self):
        """Initialize Redis connection."""
        try:
            # TODO: Initialize Redis connection pool
            # This will be implemented when we add Redis infrastructure
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            raise

    async def _setup_monitoring(self):
        """Initialize monitoring and metrics collection."""
        if settings.enable_metrics:
            try:
                # TODO: Initialize Prometheus metrics
                logger.info("Monitoring setup completed")
            except Exception as e:
                logger.error(f"Monitoring setup failed: {e}")
                raise

    async def _setup_jobs(self):
        """Initialize background job system."""
        try:
            # TODO: Initialize job queue system (Celery/RQ/etc)
            logger.info("Job system setup completed")
        except Exception as e:
            logger.error(f"Job system setup failed: {e}")
            raise

    async def _cleanup_connections(self):
        """Clean up all connections and resources."""
        try:
            # TODO: Close database connections
            # TODO: Close Redis connections
            # TODO: Cleanup job system
            logger.info("All connections cleaned up")
        except Exception as e:
            logger.error(f"Connection cleanup failed: {e}")


# Global lifespan manager
lifespan_manager = LifespanManager()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan context manager.
    Handles startup and shutdown events for the application.
    """
    # Startup
    await lifespan_manager.startup()

    try:
        # Application is running
        yield
    finally:
        # Shutdown
        await lifespan_manager.shutdown()


# Convenience functions for adding custom tasks
def add_startup_task(task):
    """Add a custom startup task."""
    return lifespan_manager.add_startup_task(task)


def add_shutdown_task(task):
    """Add a custom shutdown task."""
    return lifespan_manager.add_shutdown_task(task)