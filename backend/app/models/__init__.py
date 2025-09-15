"""
Database models using SQLAlchemy 2.0+ with async support.

This module provides database models for PostgreSQL with modern SQLAlchemy patterns:
- Async engine and session management
- Declarative base with type hints
- Relationship management
- Query optimization
"""
from typing import AsyncGenerator

from sqlalchemy import MetaData, event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core import settings, get_logger

logger = get_logger(__name__)

# Naming convention for constraints and indexes
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Provides consistent metadata configuration and naming conventions
    for all tables, constraints, and indexes.
    """
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


# Global database engine and session maker
engine: AsyncEngine = None
async_session_maker: async_sessionmaker[AsyncSession] = None


async def create_engine() -> AsyncEngine:
    """
    Create async database engine with optimized configuration.

    Returns:
        Configured async SQLAlchemy engine
    """
    global engine

    if engine is not None:
        return engine

    # Engine configuration
    engine_config = {
        "url": settings.database_url,
        "echo": settings.database_echo,  # SQL query logging
        "pool_size": settings.database_pool_size,
        "max_overflow": settings.database_max_overflow,
        "pool_timeout": settings.database_pool_timeout,
        "pool_recycle": settings.database_pool_recycle,
        "pool_pre_ping": True,  # Verify connections before use
        "future": True,  # Use SQLAlchemy 2.0 style
    }

    # Use NullPool for testing to avoid connection issues
    if settings.env == "test":
        engine_config["poolclass"] = NullPool

    engine = create_async_engine(**engine_config)

    # Log successful engine creation
    logger.info("Database engine created", extra={
        "database_url": settings.database_url.split("@")[-1],  # Hide credentials
        "pool_size": settings.database_pool_size,
        "echo": settings.database_echo,
        "environment": settings.env
    })

    return engine


async def create_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    Create async session maker with proper configuration.

    Returns:
        Configured async session maker
    """
    global async_session_maker

    if async_session_maker is not None:
        return async_session_maker

    if engine is None:
        await create_engine()

    async_session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Keep objects accessible after commit
        autoflush=True,  # Auto-flush changes before queries
        autocommit=False  # Manual transaction control
    )

    logger.info("Database session maker created")
    return async_session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.

    Provides async database session with automatic cleanup.
    Used as FastAPI dependency for database access.

    Yields:
        AsyncSession: Database session
    """
    if async_session_maker is None:
        await create_session_maker()

    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", extra={"error": str(e)})
            raise
        finally:
            await session.close()


async def init_database() -> None:
    """
    Initialize database with all tables.

    Creates all tables defined in models if they don't exist.
    Used during application startup.
    """
    try:
        if engine is None:
            await create_engine()

        # Import all models to register them with Base.metadata
        from app.models.user import User  # noqa
        from app.models.category import Category  # noqa
        from app.models.post import Post  # noqa

        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database initialization completed", extra={
            "tables_created": len(Base.metadata.tables)
        })

    except Exception as e:
        logger.error("Database initialization failed", extra={"error": str(e)})
        raise


async def close_database() -> None:
    """
    Close database connections and clean up resources.

    Used during application shutdown to properly close all connections.
    """
    global engine, async_session_maker

    try:
        if engine is not None:
            await engine.dispose()
            engine = None

        async_session_maker = None

        logger.info("Database connections closed")

    except Exception as e:
        logger.error("Database cleanup error", extra={"error": str(e)})
        raise


# Event listeners for connection management
@event.listens_for(AsyncEngine, "connect")
def set_postgresql_options(dbapi_connection, connection_record):
    """Set PostgreSQL-specific connection options."""
    # PostgreSQL specific optimizations can be added here if needed
    pass


# Export public API
__all__ = [
    "Base",
    "engine",
    "async_session_maker",
    "create_engine",
    "create_session_maker",
    "get_session",
    "init_database",
    "close_database"
]
