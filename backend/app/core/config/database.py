"""
Database Configuration Settings

Supports multiple database backends with hot-swappable configuration.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn, validator


class DatabaseSettings(BaseModel):
    """
    Database configuration with support for PostgreSQL and MongoDB.

    Allows hot-swapping between different database backends via configuration.
    """

    # Database Type Selection
    database_type: Literal["postgresql", "mongodb"] = Field(
        default="postgresql",
        description="Primary database type"
    )

    # PostgreSQL Configuration
    postgres_scheme: str = Field(default="postgresql+asyncpg", description="PostgreSQL scheme")
    postgres_user: str = Field(default="postgres", description="PostgreSQL username")
    postgres_password: str = Field(default="postgres", description="PostgreSQL password")
    postgres_host: str = Field(default="localhost", description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")
    postgres_db: str = Field(default="app", description="PostgreSQL database name")
    postgres_url: PostgresDsn | None = Field(default=None, description="Full PostgreSQL URL")

    # MongoDB Configuration
    mongodb_user: str = Field(default="mongo", description="MongoDB username")
    mongodb_password: str = Field(default="mongo", description="MongoDB password")
    mongodb_host: str = Field(default="localhost", description="MongoDB host")
    mongodb_port: int = Field(default=27017, description="MongoDB port")
    mongodb_db: str = Field(default="app", description="MongoDB database name")
    mongodb_url: str | None = Field(default=None, description="Full MongoDB URL")

    # Redis Configuration (used for caching and sessions)
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    redis_password: str | None = Field(default=None, description="Redis password")
    redis_url: RedisDsn | None = Field(default=None, description="Full Redis URL")

    # Connection Pool Settings
    pool_size: int = Field(default=20, description="Database connection pool size")
    max_overflow: int = Field(default=40, description="Maximum overflow connections")
    pool_timeout: int = Field(default=30, description="Pool connection timeout")
    pool_recycle: int = Field(default=3600, description="Connection recycle time")
    pool_pre_ping: bool = Field(default=True, description="Enable pool pre-ping")

    # Query Settings
    query_timeout: int = Field(default=30, description="Query timeout in seconds")
    slow_query_threshold: float = Field(default=1.0, description="Slow query threshold")

    # Migration Settings
    migration_timeout: int = Field(default=300, description="Migration timeout")
    auto_migration: bool = Field(default=True, description="Enable automatic migrations")

    @validator("postgres_url", pre=True)
    def assemble_postgres_connection(cls, v: str | None, values: dict) -> str:
        """Build PostgreSQL connection URL if not provided."""
        if isinstance(v, str):
            return v

        scheme = values.get("postgres_scheme", "postgresql+asyncpg")
        user = values.get("postgres_user")
        password = values.get("postgres_password")
        host = values.get("postgres_host")
        port = values.get("postgres_port", 5432)
        db = values.get("postgres_db")

        return f"{scheme}://{user}:{password}@{host}:{port}/{db}"

    @validator("mongodb_url", pre=True)
    def assemble_mongodb_connection(cls, v: str | None, values: dict) -> str:
        """Build MongoDB connection URL if not provided."""
        if isinstance(v, str):
            return v

        user = values.get("mongodb_user")
        password = values.get("mongodb_password")
        host = values.get("mongodb_host")
        port = values.get("mongodb_port", 27017)
        db = values.get("mongodb_db")

        if user and password:
            return f"mongodb://{user}:{password}@{host}:{port}/{db}"
        return f"mongodb://{host}:{port}/{db}"

    @validator("redis_url", pre=True)
    def assemble_redis_connection(cls, v: str | None, values: dict) -> str:
        """Build Redis connection URL if not provided."""
        if isinstance(v, str):
            return v

        host = values.get("redis_host")
        port = values.get("redis_port", 6379)
        db = values.get("redis_db", 0)
        password = values.get("redis_password")

        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        return f"redis://{host}:{port}/{db}"

    def get_active_url(self) -> str:
        """Get the URL for the active database type."""
        if self.database_type == "postgresql":
            return str(self.postgres_url)
        elif self.database_type == "mongodb":
            return str(self.mongodb_url)
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")

    def get_connection_params(self) -> dict:
        """Get connection parameters for the active database."""
        base_params = {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "pool_pre_ping": self.pool_pre_ping,
        }

        if self.database_type == "postgresql":
            base_params.update({
                "echo": False,  # Set to True for SQL logging in development
                "echo_pool": False,  # Pool event logging
                "future": True,  # Use SQLAlchemy 2.0 style
            })

        return base_params

    @property
    def is_postgresql(self) -> bool:
        """Check if PostgreSQL is the active database."""
        return self.database_type == "postgresql"

    @property
    def is_mongodb(self) -> bool:
        """Check if MongoDB is the active database."""
        return self.database_type == "mongodb"