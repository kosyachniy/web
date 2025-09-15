"""
Application settings using pydantic-settings v2.
All configuration loaded from environment variables with APP_ prefix.
"""
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation and type conversion."""

    # App Configuration
    env: str = Field(default="dev", description="Environment: dev/test/prod")
    debug: bool = Field(default=True, description="Debug mode")
    name: str = Field(default="Backend API", description="Application name")
    version: str = Field(default="2.0.0", description="Application version")

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # PostgreSQL Database Configuration
    database_url: str = Field(
        description="PostgreSQL database connection URL",
        examples=[
            "postgresql+asyncpg://user:password@localhost:5432/mydb",
            "postgresql+asyncpg://user:password@db:5432/production_db"
        ]
    )
    database_echo: bool = Field(
        default=False,
        description="Enable SQLAlchemy query logging for debugging"
    )
    database_pool_size: int = Field(
        default=20,
        description="Database connection pool size"
    )
    database_max_overflow: int = Field(
        default=10,
        description="Maximum overflow connections beyond pool size"
    )
    database_pool_timeout: int = Field(
        default=30,
        description="Timeout for getting connection from pool (seconds)"
    )
    database_pool_recycle: int = Field(
        default=3600,
        description="Recycle connections after N seconds to avoid stale connections"
    )

    # Redis Configuration
    redis_url: str = Field(description="Redis connection URL")
    redis_max_connections: int = Field(default=50, description="Redis max connections")

    # Authentication & Security
    jwt_secret: str = Field(description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration")

    # API Configuration
    api_prefix: str = Field(default="/v1", description="API route prefix")
    cors_origins: List[str] = Field(default=["*"], description="CORS allowed origins")

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=100, description="Requests per minute limit")
    rate_limit_burst: int = Field(default=200, description="Burst limit for rate limiting")

    # Background Jobs
    queue_backend: str = Field(default="redis", description="Queue backend: redis/celery")
    celery_broker_url: Optional[str] = Field(default=None, description="Celery broker URL")
    celery_result_backend: Optional[str] = Field(default=None, description="Celery result backend")

    # External Services
    telegram_bot_token: Optional[str] = Field(default=None, description="Telegram bot token")

    # Monitoring & Observability
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json/text")

    # File Storage
    storage_type: str = Field(default="local", description="Storage type: local/s3")
    s3_bucket: Optional[str] = Field(default=None, description="S3 bucket name")
    s3_region: Optional[str] = Field(default=None, description="S3 region")
    upload_max_size: int = Field(default=10 * 1024 * 1024, description="Max upload size in bytes")

    model_config = {
        "env_prefix": "APP_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Ignore extra fields not defined in model
    }


# Global settings instance
settings = Settings()


# Environment helpers
def is_development() -> bool:
    """Check if running in development mode."""
    return settings.env.lower() in ("dev", "development")


def is_production() -> bool:
    """Check if running in production mode."""
    return settings.env.lower() in ("prod", "production")


def is_testing() -> bool:
    """Check if running in test mode."""
    return settings.env.lower() in ("test", "testing")