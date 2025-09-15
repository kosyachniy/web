"""
User-related Pydantic schemas for authentication and profile management.

Provides comprehensive schemas for user operations:
- Authentication (register, login, token management)
- Profile management (create, update, view)
- Admin operations (user lists, moderation)
- Permission and status management
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field, EmailStr, field_validator, model_validator

from app.schemas.base import BaseSchema, TimestampSchema, PaginatedResponseSchema


class UserStatus(str, Enum):
    """User status enumeration for API responses."""
    DELETED = "deleted"
    BLOCKED = "blocked"
    PENDING = "pending"
    ACTIVE = "active"
    VERIFIED = "verified"
    MODERATOR = "moderator"
    ADMIN = "admin"
    OWNER = "owner"


class Gender(str, Enum):
    """Gender enumeration for API responses."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


# Authentication Schemas

class LoginRequestSchema(BaseSchema):
    """Schema for user login requests."""

    email: EmailStr = Field(
        description="User email address",
        examples=["user@example.com", "john.doe@company.com"]
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password",
        examples=["SecurePassword123!"]
    )


class TokenResponseSchema(BaseSchema):
    """Schema for authentication token responses."""

    access_token: str = Field(
        description="JWT access token for API authentication"
    )

    refresh_token: str = Field(
        description="JWT refresh token for token renewal"
    )

    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')"
    )

    expires_in: int = Field(
        gt=0,
        description="Access token expiration time in seconds",
        examples=[1800, 3600]
    )


# User Management Schemas

class UserCreateSchema(BaseSchema):
    """Schema for creating new user accounts."""

    email: EmailStr = Field(
        description="User email address (must be unique)",
        examples=["user@example.com", "john.doe@company.com"]
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password (will be hashed)",
        examples=["SecurePassword123!"]
    )

    full_name: str = Field(
        min_length=2,
        max_length=255,
        description="User's full name",
        examples=["John Doe", "Jane Smith"]
    )

    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Unique username (alphanumeric, underscore, hyphen only)",
        examples=["john_doe", "jane-smith", "user123"]
    )

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain uppercase, lowercase, and numeric characters')

        return v

    @field_validator('username')
    @classmethod
    def validate_username_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate username format and restrictions."""
        if v is None:
            return v

        if v.lower() in ['admin', 'root', 'system', 'api', 'www', 'mail']:
            raise ValueError('Username is reserved')

        return v.lower()


class UserUpdateSchema(BaseSchema):
    """Schema for updating user profile information."""

    full_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
        description="User's full name",
        examples=["John Doe", "Jane Smith"]
    )

    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r'^[a-zA-Z0-9_-]+$',
        description="Unique username",
        examples=["john_doe", "jane-smith"]
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=500,
        description="User biography/description",
        examples=["Software developer passionate about Python and AI"]
    )

    phone: Optional[str] = Field(
        default=None,
        max_length=20,
        pattern=r'^\+?[1-9]\d{1,14}$',
        description="Phone number in international format",
        examples=["+1234567890", "+44123456789"]
    )

    birth_date: Optional[str] = Field(
        default=None,
        pattern=r'^\d{2}\.\d{2}\.\d{4}$',
        description="Birth date in DD.MM.YYYY format",
        examples=["15.01.1990", "31.12.1985"]
    )

    gender: Optional[Gender] = Field(
        default=None,
        description="User's gender"
    )

    avatar_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="URL to user's avatar image",
        examples=["https://example.com/avatar.jpg"]
    )

    preferences: Optional[Dict[str, Any]] = Field(
        default=None,
        description="User preferences and settings",
        examples=[{"theme": "dark", "language": "en", "notifications": True}]
    )

    notification_settings: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Notification preferences",
        examples=[{"email_notifications": True, "push_notifications": False}]
    )


class PasswordChangeSchema(BaseSchema):
    """Schema for changing user password."""

    current_password: str = Field(
        description="Current password for verification",
        examples=["CurrentPassword123!"]
    )

    new_password: str = Field(
        min_length=8,
        max_length=128,
        description="New password",
        examples=["NewSecurePassword123!"]
    )

    @field_validator('new_password')
    @classmethod
    def validate_new_password_strength(cls, v: str) -> str:
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain uppercase, lowercase, and numeric characters')

        return v

    @model_validator(mode='after')
    def validate_passwords_different(self) -> 'PasswordChangeSchema':
        """Ensure new password is different from current password."""
        if self.current_password == self.new_password:
            raise ValueError('New password must be different from current password')
        return self


# Response Schemas

class UserResponseSchema(BaseSchema, TimestampSchema):
    """Schema for detailed user information responses."""

    id: int = Field(
        description="User ID",
        examples=[1, 42, 123]
    )

    email: EmailStr = Field(
        description="User email address",
        examples=["user@example.com"]
    )

    full_name: str = Field(
        description="User's full name",
        examples=["John Doe"]
    )

    username: Optional[str] = Field(
        default=None,
        description="User's username",
        examples=["john_doe"]
    )

    bio: Optional[str] = Field(
        default=None,
        description="User biography",
        examples=["Software developer passionate about Python"]
    )

    avatar_url: Optional[str] = Field(
        default=None,
        description="User's avatar image URL",
        examples=["https://example.com/avatar.jpg"]
    )

    phone: Optional[str] = Field(
        default=None,
        description="User's phone number",
        examples=["+1234567890"]
    )

    birth_date: Optional[str] = Field(
        default=None,
        description="Birth date in DD.MM.YYYY format",
        examples=["15.01.1990"]
    )

    gender: Optional[Gender] = Field(
        default=None,
        description="User's gender"
    )

    status: UserStatus = Field(
        description="User account status",
        examples=["active", "verified"]
    )

    is_active: bool = Field(
        description="Whether user account is active",
        examples=[True, False]
    )

    email_verified: bool = Field(
        description="Email verification status",
        examples=[True, False]
    )

    phone_verified: bool = Field(
        description="Phone verification status",
        examples=[True, False]
    )

    subscription_tier: int = Field(
        description="User subscription tier level",
        examples=[0, 1, 2, 3]
    )

    last_login_at: Optional[str] = Field(
        default=None,
        description="Last login timestamp in DD.MM.YYYY HH:MM:SS format",
        examples=["15.01.2024 14:30:00"]
    )


class UserProfileSchema(BaseSchema):
    """Schema for public user profile information (limited data)."""

    id: int = Field(
        description="User ID",
        examples=[1, 42, 123]
    )

    full_name: str = Field(
        description="User's full name",
        examples=["John Doe"]
    )

    username: Optional[str] = Field(
        default=None,
        description="User's username",
        examples=["john_doe"]
    )

    bio: Optional[str] = Field(
        default=None,
        description="User biography",
        examples=["Software developer passionate about Python"]
    )

    avatar_url: Optional[str] = Field(
        default=None,
        description="User's avatar image URL",
        examples=["https://example.com/avatar.jpg"]
    )

    created_at: str = Field(
        description="Registration date in DD.MM.YYYY format",
        examples=["01.01.2024"]
    )


# Admin Schemas

class AdminUserResponseSchema(UserResponseSchema):
    """Schema for admin view of user information (includes sensitive data)."""

    login_count: int = Field(
        description="Total number of logins",
        examples=[0, 15, 142]
    )

    failed_login_attempts: int = Field(
        description="Number of consecutive failed login attempts",
        examples=[0, 1, 3]
    )

    posts_count: int = Field(
        default=0,
        description="Number of posts created by user",
        examples=[0, 5, 23]
    )

    balance: float = Field(
        description="User account balance",
        examples=[0.0, 25.99, 150.50]
    )

    utm_source: Optional[str] = Field(
        default=None,
        description="UTM source for user acquisition tracking",
        examples=["google", "facebook", "direct"]
    )

    referral_code: Optional[str] = Field(
        default=None,
        description="User's referral code",
        examples=["REF123", "JOHN2024"]
    )

    referred_by: Optional[int] = Field(
        default=None,
        description="ID of user who referred this user",
        examples=[42, 123]
    )

    is_deleted: bool = Field(
        description="Soft delete status",
        examples=[False, True]
    )

    deleted_at: Optional[str] = Field(
        default=None,
        description="Soft delete timestamp",
        examples=["15.01.2024 16:30:00"]
    )


class UserModerationSchema(BaseSchema):
    """Schema for user moderation actions."""

    action: str = Field(
        pattern="^(activate|deactivate|verify|unverify|block|unblock|delete|restore)$",
        description="Moderation action to perform",
        examples=["activate", "block", "verify"]
    )

    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Reason for moderation action",
        examples=["Account verification completed", "Suspicious activity detected"]
    )

    duration_days: Optional[int] = Field(
        default=None,
        gt=0,
        le=365,
        description="Duration for temporary actions (in days)",
        examples=[7, 30, 90]
    )


# List Response Schemas

class UserListResponseSchema(PaginatedResponseSchema[UserResponseSchema]):
    """Schema for paginated user list responses."""
    pass


class AdminUserListResponseSchema(PaginatedResponseSchema[AdminUserResponseSchema]):
    """Schema for admin paginated user list responses."""
    pass


# Statistics Schemas

class UserStatsSchema(BaseSchema):
    """Schema for user statistics."""

    total_users: int = Field(
        description="Total number of users",
        examples=[1250, 5000, 10000]
    )

    active_users: int = Field(
        description="Number of active users",
        examples=[1200, 4800, 9500]
    )

    verified_users: int = Field(
        description="Number of verified users",
        examples=[800, 3500, 7000]
    )

    new_users_today: int = Field(
        description="Number of new users registered today",
        examples=[5, 25, 100]
    )

    new_users_this_week: int = Field(
        description="Number of new users registered this week",
        examples=[35, 175, 700]
    )

    new_users_this_month: int = Field(
        description="Number of new users registered this month",
        examples=[150, 750, 3000]
    )