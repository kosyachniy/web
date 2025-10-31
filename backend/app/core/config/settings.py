"""
Main Application Settings

Centralized configuration management using Pydantic Settings with
environment variable validation and type safety.
"""

from __future__ import annotations

import secrets
from enum import Enum
from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseSettings
from .security import SecuritySettings
from .monitoring import MonitoringSettings
from .external_apis import ExternalAPISettings


class Environment(str, Enum):
    """Application environment types."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class Settings(BaseSettings):
    """
    Main application settings with environment-specific configuration.

    All settings can be overridden via environment variables with the
    APP_ prefix (e.g., APP_DEBUG=true).
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
        extra="ignore"
    )

    # Basic Application Settings
    app_name: str = Field(default="Modern Backend API", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Runtime environment")

    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=1, description="Number of worker processes")

    # API Configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 path prefix")
    docs_url: str | None = Field(default="/docs", description="Swagger docs URL")
    redoc_url: str | None = Field(default="/redoc", description="ReDoc URL")
    openapi_url: str | None = Field(default="/openapi.json", description="OpenAPI spec URL")

    # CORS Configuration
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials in CORS")
    cors_methods: list[str] = Field(default=["*"], description="Allowed CORS methods")
    cors_headers: list[str] = Field(default=["*"], description="Allowed CORS headers")

    # Logging Configuration
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    log_format: str = Field(default="json", description="Log format (json|text)")
    log_file: str | None = Field(default=None, description="Log file path")

    # Feature Flags
    enable_docs: bool = Field(default=True, description="Enable API documentation")
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    enable_tracing: bool = Field(default=True, description="Enable distributed tracing")
    enable_profiling: bool = Field(default=False, description="Enable performance profiling")

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    default_rate_limit: str = Field(default="100/minute", description="Default rate limit")

    # Background Tasks
    celery_broker_url: RedisDsn | None = Field(default=None, description="Celery broker URL")
    celery_result_backend: RedisDsn | None = Field(default=None, description="Celery result backend")

    # Message Broker Configuration
    message_broker_type: Literal["rabbitmq", "redis", "memory"] = Field(
        default="redis", description="Message broker type"
    )
    rabbitmq_url: str | None = Field(default=None, description="RabbitMQ connection URL")

    # External Service URLs
    frontend_url: str = Field(default="http://localhost:3000", description="Frontend URL")

    # Nested Settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    external_apis: ExternalAPISettings = Field(default_factory=ExternalAPISettings)

    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError("Invalid CORS origins format")

    @validator("docs_url")
    def disable_docs_in_production(cls, v: str | None, values: dict) -> str | None:
        """Disable docs in production unless explicitly enabled."""
        if values.get("environment") == Environment.PRODUCTION:
            if not values.get("enable_docs", False):
                return None
        return v

    @validator("openapi_url")
    def disable_openapi_in_production(cls, v: str | None, values: dict) -> str | None:
        """Disable OpenAPI spec in production unless explicitly enabled."""
        if values.get("environment") == Environment.PRODUCTION:
            if not values.get("enable_docs", False):
                return None
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.environment == Environment.TESTING

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == Environment.PRODUCTION

    @property
    def server_host_port(self) -> str:
        """Get server host:port string."""
        return f"{self.host}:{self.port}"

    def get_database_url(self) -> str:
        """Get the active database URL."""
        return self.database.get_active_url()

    def get_cache_url(self) -> str:
        """Get the Redis cache URL."""
        return str(self.database.redis_url)


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings.

    Uses LRU cache to avoid re-parsing environment variables
    on every function call.
    """
    return Settings()