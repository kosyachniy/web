"""
Application Lifespan Management

Handles FastAPI application startup and shutdown events with proper
resource initialization and cleanup.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from loguru import logger

from app.core.config import get_settings
from app.core.container import container, wire_container
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan context manager.

    Handles application startup and shutdown events with proper
    resource management and error handling.
    """
    settings = get_settings()

    # Startup
    logger.info("🚀 Starting application initialization...")

    try:
        # Setup logging first
        await setup_logging(settings)
        logger.info("✅ Logging configured")

        # Configure dependency injection
        container.config.from_pydantic(settings)
        wire_container()
        logger.info("✅ Dependency injection configured")

        # Initialize database
        await initialize_database(settings)
        logger.info("✅ Database initialized")

        # Initialize cache
        await initialize_cache(settings)
        logger.info("✅ Cache initialized")

        # Initialize message broker
        await initialize_message_broker(settings)
        logger.info("✅ Message broker initialized")

        # Initialize monitoring
        await initialize_monitoring(settings)
        logger.info("✅ Monitoring initialized")

        # Initialize background tasks
        await initialize_background_tasks(settings)
        logger.info("✅ Background tasks initialized")

        # Run health checks
        await run_startup_health_checks()
        logger.info("✅ Health checks passed")

        logger.info("🎉 Application startup completed successfully")

        yield

    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise

    finally:
        # Shutdown
        logger.info("🛑 Starting application shutdown...")

        try:
            # Shutdown background tasks
            await shutdown_background_tasks()
            logger.info("✅ Background tasks shutdown")

            # Shutdown message broker
            await shutdown_message_broker()
            logger.info("✅ Message broker shutdown")

            # Shutdown cache
            await shutdown_cache()
            logger.info("✅ Cache shutdown")

            # Shutdown database
            await shutdown_database()
            logger.info("✅ Database shutdown")

            # Shutdown monitoring
            await shutdown_monitoring()
            logger.info("✅ Monitoring shutdown")

            logger.info("👋 Application shutdown completed successfully")

        except Exception as e:
            logger.error(f"❌ Error during application shutdown: {e}")
            # Don't re-raise shutdown errors


async def initialize_database(settings: Any) -> None:
    """Initialize database connections and run migrations."""
    try:
        # Get database engine from container
        database_engine = container.database_engine()

        # Test connection
        if settings.database.database_type == "postgresql":
            await test_postgresql_connection(database_engine)
        elif settings.database.database_type == "mongodb":
            await test_mongodb_connection(database_engine)

        # Run migrations if enabled
        if settings.database.auto_migration:
            await run_database_migrations(settings)

        logger.info(f"Database ({settings.database.database_type}) connection established")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def initialize_cache(settings: Any) -> None:
    """Initialize Redis cache connection."""
    try:
        redis_client = container.redis_client()

        # Test Redis connection
        await redis_client.ping()

        logger.info("Redis cache connection established")

    except Exception as e:
        logger.error(f"Cache initialization failed: {e}")
        raise


async def initialize_message_broker(settings: Any) -> None:
    """Initialize message broker connection."""
    try:
        if settings.message_broker_type == "memory":
            logger.info("Using in-memory message broker")
            return

        message_broker = container.message_broker()

        # Test broker connection
        await message_broker.connect()

        logger.info(f"Message broker ({settings.message_broker_type}) connection established")

    except Exception as e:
        logger.error(f"Message broker initialization failed: {e}")
        raise


async def initialize_monitoring(settings: Any) -> None:
    """Initialize monitoring and observability."""
    try:
        if settings.monitoring.metrics_enabled:
            metrics_collector = container.metrics_collector()
            await metrics_collector.initialize()
            logger.info("Metrics collection initialized")

        if settings.monitoring.tracing_enabled:
            tracer = container.tracer()
            await tracer.initialize()
            logger.info("Distributed tracing initialized")

    except Exception as e:
        logger.error(f"Monitoring initialization failed: {e}")
        # Don't fail startup for monitoring issues
        logger.warning("Continuing without full monitoring setup")


async def initialize_background_tasks(settings: Any) -> None:
    """Initialize background task processing."""
    try:
        if settings.celery_broker_url:
            task_broker = container.task_broker()
            # Celery broker is initialized lazily
            logger.info("Celery task broker configured")

        scheduler = container.scheduler()
        scheduler.start()
        logger.info("Task scheduler started")

    except Exception as e:
        logger.error(f"Background tasks initialization failed: {e}")
        raise


async def run_startup_health_checks() -> None:
    """Run comprehensive health checks on startup."""
    try:
        health_checker = container.health_checker()
        health_status = await health_checker.check_all()

        if not health_status.is_healthy:
            unhealthy_services = [
                service for service, status in health_status.checks.items()
                if not status.is_healthy
            ]
            raise RuntimeError(
                f"Health check failed for services: {', '.join(unhealthy_services)}"
            )

        logger.info("All health checks passed")

    except Exception as e:
        logger.error(f"Health checks failed: {e}")
        raise


async def test_postgresql_connection(engine: Any) -> None:
    """Test PostgreSQL database connection."""
    from sqlalchemy import text

    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


async def test_mongodb_connection(client: Any) -> None:
    """Test MongoDB database connection."""
    # MongoDB connection test will be implemented
    # when we create the MongoDB adapter
    await client.admin.command("ping")


async def run_database_migrations(settings: Any) -> None:
    """Run database migrations."""
    if settings.database.database_type == "postgresql":
        # Run Alembic migrations
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed")


# Shutdown functions

async def shutdown_background_tasks() -> None:
    """Shutdown background task processing."""
    try:
        scheduler = container.scheduler()
        scheduler.shutdown(wait=True)

        # Shutdown Celery workers gracefully
        # This will be implemented when we create the Celery integration

    except Exception as e:
        logger.error(f"Error shutting down background tasks: {e}")


async def shutdown_message_broker() -> None:
    """Shutdown message broker connections."""
    try:
        message_broker = container.message_broker()
        await message_broker.disconnect()

    except Exception as e:
        logger.error(f"Error shutting down message broker: {e}")


async def shutdown_cache() -> None:
    """Shutdown Redis cache connections."""
    try:
        redis_client = container.redis_client()
        await redis_client.close()

    except Exception as e:
        logger.error(f"Error shutting down cache: {e}")


async def shutdown_database() -> None:
    """Shutdown database connections."""
    try:
        database_engine = container.database_engine()
        await database_engine.dispose()

    except Exception as e:
        logger.error(f"Error shutting down database: {e}")


async def shutdown_monitoring() -> None:
    """Shutdown monitoring services."""
    try:
        # Shutdown metrics collection
        if container.metrics_collector.provided:
            metrics_collector = container.metrics_collector()
            await metrics_collector.shutdown()

        # Shutdown tracing
        if container.tracer.provided:
            tracer = container.tracer()
            await tracer.shutdown()

    except Exception as e:
        logger.error(f"Error shutting down monitoring: {e}")