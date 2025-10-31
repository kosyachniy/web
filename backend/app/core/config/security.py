"""
Security Configuration Settings

Advanced security configuration supporting multiple authentication strategies,
rate limiting, and encryption settings.
"""

from __future__ import annotations

import secrets
from typing import Literal

from pydantic import BaseModel, Field, validator


class SecuritySettings(BaseModel):
    """
    Security configuration with multiple authentication strategies
    and comprehensive protection mechanisms.
    """

    # JWT Configuration
    jwt_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="JWT secret key"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration (minutes)"
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7, description="Refresh token expiration (days)"
    )
    jwt_issuer: str = Field(default="modern-backend", description="JWT issuer")
    jwt_audience: str = Field(default="modern-backend-users", description="JWT audience")

    # Password Configuration
    password_min_length: int = Field(default=8, description="Minimum password length")
    password_require_uppercase: bool = Field(default=True, description="Require uppercase")
    password_require_lowercase: bool = Field(default=True, description="Require lowercase")
    password_require_digits: bool = Field(default=True, description="Require digits")
    password_require_special: bool = Field(default=True, description="Require special chars")
    bcrypt_rounds: int = Field(default=12, description="Bcrypt hashing rounds")

    # API Key Configuration
    api_key_header_name: str = Field(default="X-API-Key", description="API key header")
    api_key_prefix: str = Field(default="mbapi_", description="API key prefix")
    api_key_length: int = Field(default=32, description="API key length")

    # OAuth2 Configuration
    oauth2_enabled: bool = Field(default=False, description="Enable OAuth2")
    google_client_id: str | None = Field(default=None, description="Google OAuth2 client ID")
    google_client_secret: str | None = Field(
        default=None, description="Google OAuth2 client secret"
    )
    github_client_id: str | None = Field(default=None, description="GitHub OAuth2 client ID")
    github_client_secret: str | None = Field(
        default=None, description="GitHub OAuth2 client secret"
    )

    # Session Configuration
    session_cookie_name: str = Field(default="session", description="Session cookie name")
    session_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Session secret key"
    )
    session_cookie_secure: bool = Field(default=True, description="Secure session cookies")
    session_cookie_httponly: bool = Field(default=True, description="HTTP-only cookies")
    session_cookie_samesite: Literal["strict", "lax", "none"] = Field(
        default="lax", description="SameSite cookie policy"
    )
    session_expire_hours: int = Field(default=24, description="Session expiration (hours)")

    # Rate Limiting Configuration
    rate_limit_storage: Literal["redis", "memory"] = Field(
        default="redis", description="Rate limit storage backend"
    )
    rate_limit_key_prefix: str = Field(default="rl:", description="Rate limit key prefix")

    # Default rate limits by endpoint type
    auth_rate_limit: str = Field(default="5/minute", description="Auth endpoint rate limit")
    api_rate_limit: str = Field(default="100/minute", description="API endpoint rate limit")
    public_rate_limit: str = Field(default="1000/hour", description="Public endpoint rate limit")

    # Security Headers
    enable_security_headers: bool = Field(default=True, description="Enable security headers")
    hsts_max_age: int = Field(default=31536000, description="HSTS max age")
    csp_policy: str = Field(
        default="default-src 'self'", description="Content Security Policy"
    )

    # CORS Security
    cors_max_age: int = Field(default=86400, description="CORS preflight cache time")
    cors_allow_credentials: bool = Field(default=True, description="Allow CORS credentials")

    # Encryption Configuration
    encryption_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Application encryption key"
    )
    fernet_key: str | None = Field(default=None, description="Fernet encryption key")

    # Request Validation
    max_request_size: int = Field(default=16 * 1024 * 1024, description="Max request size")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Max file upload size")
    allowed_file_extensions: list[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".csv"],
        description="Allowed file extensions"
    )

    # IP Security
    trusted_proxies: list[str] = Field(default=[], description="Trusted proxy IPs")
    blocked_ips: list[str] = Field(default=[], description="Blocked IP addresses")
    ip_whitelist: list[str] = Field(default=[], description="IP whitelist")

    # Audit and Monitoring
    log_failed_auth_attempts: bool = Field(
        default=True, description="Log failed authentication attempts"
    )
    failed_auth_lockout_attempts: int = Field(
        default=5, description="Failed auth attempts before lockout"
    )
    failed_auth_lockout_duration: int = Field(
        default=900, description="Auth lockout duration (seconds)"
    )

    @validator("jwt_secret_key")
    def validate_jwt_secret_strength(cls, v: str) -> str:
        """Validate JWT secret key strength."""
        if len(v) < 32:
            raise ValueError("JWT secret key must be at least 32 characters")
        return v

    @validator("session_secret_key")
    def validate_session_secret_strength(cls, v: str) -> str:
        """Validate session secret key strength."""
        if len(v) < 32:
            raise ValueError("Session secret key must be at least 32 characters")
        return v

    @validator("bcrypt_rounds")
    def validate_bcrypt_rounds(cls, v: int) -> int:
        """Validate bcrypt rounds for security vs performance balance."""
        if v < 10:
            raise ValueError("Bcrypt rounds should be at least 10 for security")
        if v > 15:
            raise ValueError("Bcrypt rounds above 15 may cause performance issues")
        return v

    @property
    def jwt_access_token_expire_seconds(self) -> int:
        """Get JWT access token expiration in seconds."""
        return self.jwt_access_token_expire_minutes * 60

    @property
    def jwt_refresh_token_expire_seconds(self) -> int:
        """Get JWT refresh token expiration in seconds."""
        return self.jwt_refresh_token_expire_days * 24 * 60 * 60

    @property
    def session_expire_seconds(self) -> int:
        """Get session expiration in seconds."""
        return self.session_expire_hours * 60 * 60

    def get_password_requirements(self) -> dict[str, bool]:
        """Get password requirement flags."""
        return {
            "min_length": self.password_min_length,
            "require_uppercase": self.password_require_uppercase,
            "require_lowercase": self.password_require_lowercase,
            "require_digits": self.password_require_digits,
            "require_special": self.password_require_special,
        }

    def is_oauth2_configured(self) -> bool:
        """Check if OAuth2 is properly configured."""
        return (
            self.oauth2_enabled
            and (
                (self.google_client_id and self.google_client_secret)
                or (self.github_client_id and self.github_client_secret)
            )
        )