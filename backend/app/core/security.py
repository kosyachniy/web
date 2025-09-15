"""
Security utilities for authentication, password hashing, and JWT token management.
Provides secure defaults for cryptographic operations.
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union

import jwt
from passlib.context import CryptContext
from passlib.exc import InvalidTokenError as PasslibInvalidTokenError

from .settings import settings
from .logging import get_logger

logger = get_logger(__name__)


# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Good security/performance balance
)


class SecurityError(Exception):
    """Base exception for security-related errors."""
    pass


class InvalidTokenError(SecurityError):
    """Raised when a JWT token is invalid."""
    pass


class ExpiredTokenError(SecurityError):
    """Raised when a JWT token has expired."""
    pass


class TokenManager:
    """JWT token management utilities."""

    def __init__(self):
        self.secret_key = settings.jwt_secret
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire = timedelta(minutes=settings.access_token_expire_minutes)
        self.refresh_token_expire = timedelta(days=settings.refresh_token_expire_days)

    def create_access_token(
        self,
        subject: Union[str, int],
        expires_delta: Optional[timedelta] = None,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a JWT access token.

        Args:
            subject: User ID or identifier
            expires_delta: Custom expiration time
            additional_claims: Additional claims to include in token

        Returns:
            JWT token string
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.access_token_expire

        payload = {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
            "jti": secrets.token_hex(16),  # JWT ID for token tracking
        }

        if additional_claims:
            payload.update(additional_claims)

        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.debug("Access token created", extra={
                "subject": subject,
                "expires": expire.isoformat(),
                "jti": payload["jti"]
            })
            return token
        except Exception as e:
            logger.error("Failed to create access token", extra={"error": str(e)})
            raise SecurityError("Failed to create access token") from e

    def create_refresh_token(
        self,
        subject: Union[str, int],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT refresh token.

        Args:
            subject: User ID or identifier
            expires_delta: Custom expiration time

        Returns:
            JWT refresh token string
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + self.refresh_token_expire

        payload = {
            "sub": str(subject),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_hex(16),
        }

        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            logger.debug("Refresh token created", extra={
                "subject": subject,
                "expires": expire.isoformat(),
                "jti": payload["jti"]
            })
            return token
        except Exception as e:
            logger.error("Failed to create refresh token", extra={"error": str(e)})
            raise SecurityError("Failed to create refresh token") from e

    def decode_token(self, token: str, token_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.

        Args:
            token: JWT token string
            token_type: Expected token type ("access" or "refresh")

        Returns:
            Decoded token payload

        Raises:
            InvalidTokenError: Token is invalid
            ExpiredTokenError: Token has expired
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"require": ["sub", "exp", "iat", "type"]}
            )

            # Validate token type if specified
            if token_type and payload.get("type") != token_type:
                logger.warning("Token type mismatch", extra={
                    "expected": token_type,
                    "actual": payload.get("type"),
                    "jti": payload.get("jti")
                })
                raise InvalidTokenError("Invalid token type")

            logger.debug("Token decoded successfully", extra={
                "subject": payload.get("sub"),
                "type": payload.get("type"),
                "jti": payload.get("jti")
            })

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise ExpiredTokenError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid token", extra={"error": str(e)})
            raise InvalidTokenError("Invalid token") from e

    def get_token_subject(self, token: str) -> str:
        """
        Extract subject (user ID) from token without full validation.
        Useful for logging purposes.
        """
        try:
            # Decode without verification for subject extraction
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload.get("sub", "unknown")
        except Exception:
            return "unknown"


class PasswordManager:
    """Password hashing and verification utilities."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        try:
            hashed = pwd_context.hash(password)
            logger.debug("Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error("Password hashing failed", extra={"error": str(e)})
            raise SecurityError("Password hashing failed") from e

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: Plain text password
            hashed_password: Hashed password from database

        Returns:
            True if password matches, False otherwise
        """
        try:
            is_valid = pwd_context.verify(password, hashed_password)
            logger.debug("Password verification completed", extra={"valid": is_valid})
            return is_valid
        except (PasslibInvalidTokenError, ValueError) as e:
            logger.warning("Password verification failed", extra={"error": str(e)})
            return False
        except Exception as e:
            logger.error("Unexpected error during password verification", extra={"error": str(e)})
            return False

    @staticmethod
    def generate_random_password(length: int = 16) -> str:
        """
        Generate a cryptographically secure random password.

        Args:
            length: Password length

        Returns:
            Random password string
        """
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        logger.debug("Random password generated", extra={"length": length})
        return password


class SecurityUtils:
    """General security utilities."""

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: Token length in bytes

        Returns:
            Hex-encoded token string
        """
        token = secrets.token_hex(length)
        logger.debug("Secure token generated", extra={"length": length * 2})  # hex doubles length
        return token

    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key."""
        return f"ak_{secrets.token_hex(24)}"  # 48 char hex string with prefix

    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        """
        Compare two strings in constant time to prevent timing attacks.

        Args:
            a: First string
            b: Second string

        Returns:
            True if strings are equal, False otherwise
        """
        return secrets.compare_digest(a.encode(), b.encode())


# Global instances
token_manager = TokenManager()
password_manager = PasswordManager()
security_utils = SecurityUtils()


# Convenience functions
def create_access_token(subject: Union[str, int], **kwargs) -> str:
    """Create an access token."""
    return token_manager.create_access_token(subject, **kwargs)


def create_refresh_token(subject: Union[str, int], **kwargs) -> str:
    """Create a refresh token."""
    return token_manager.create_refresh_token(subject, **kwargs)


def decode_token(token: str, token_type: Optional[str] = None) -> Dict[str, Any]:
    """Decode a JWT token."""
    return token_manager.decode_token(token, token_type)


def hash_password(password: str) -> str:
    """Hash a password."""
    return password_manager.hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password."""
    return password_manager.verify_password(password, hashed_password)