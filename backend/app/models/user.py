"""
User model for authentication and profile management.

Represents users in the system with authentication, profile, and permission management.
Uses modern SQLAlchemy patterns with async support and comprehensive field validation.
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlalchemy import String, Boolean, Integer, DateTime, Text, JSON, Float, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class UserStatus(Enum):
    """User status enumeration with clear hierarchy."""
    DELETED = 0      # Soft deleted user
    BLOCKED = 1      # Blocked user - cannot access system
    PENDING = 2      # Pending email verification
    ACTIVE = 3       # Active user with basic access
    VERIFIED = 4     # Verified user with full platform access
    MODERATOR = 5    # User with moderation privileges
    ADMIN = 6        # User with administrative privileges
    OWNER = 7        # System owner with full privileges


class Gender(Enum):
    """Gender enumeration."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class User(BaseModel, SoftDeleteMixin):
    """
    User model with comprehensive profile and authentication fields.

    Provides user management with:
    - Authentication (email/password)
    - Profile information (name, bio, etc.)
    - Status and permission management
    - Social media integration
    - Subscription and billing
    - Activity tracking
    """

    __tablename__ = "users"

    # Primary identification
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Authentication
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        doc="User email address (primary login)"
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Hashed password using bcrypt"
    )

    # Profile Information
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="User's full name"
    )

    username: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
        doc="Unique username for public profile"
    )

    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="User biography/description"
    )

    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="URL to user's avatar image"
    )

    birth_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="User's birth date"
    )

    gender: Mapped[Optional[Gender]] = mapped_column(
        SQLEnum(Gender),
        nullable=True,
        doc="User's gender"
    )

    # Contact Information
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        doc="User's phone number"
    )

    phone_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Phone number verification status"
    )

    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Email verification status"
    )

    # System Status and Permissions
    status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus),
        default=UserStatus.PENDING,
        nullable=False,
        index=True,
        doc="User status determining access level"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        doc="Whether user account is active"
    )

    # Social and External Integrations
    social_profiles: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        doc="Social media profiles and external accounts"
    )

    # Subscription and Billing
    subscription_tier: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="User subscription tier level"
    )

    balance: Mapped[float] = mapped_column(
        Float(precision=2),
        default=0.0,
        nullable=False,
        doc="User account balance"
    )

    # Marketing and Analytics
    utm_source: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="UTM source for user acquisition tracking"
    )

    referral_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
        doc="User's unique referral code"
    )

    referred_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="ID of user who referred this user"
    )

    # User Preferences
    preferences: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        doc="User preferences and settings"
    )

    notification_settings: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        doc="Notification preferences"
    )

    # Activity Tracking
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last successful login timestamp"
    )

    login_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Total number of logins"
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of consecutive failed login attempts"
    )

    password_changed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="When password was last changed"
    )

    # Relationships
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="author",
        lazy="select",
        cascade="all, delete-orphan"
    )

    # Table indexes for performance
    __table_args__ = (
        Index("idx_users_email_active", "email", "is_active"),
        Index("idx_users_status_created", "status", "created_at"),
        Index("idx_users_last_login", "last_login_at"),
    )

    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.status in (UserStatus.ADMIN, UserStatus.OWNER)

    def is_moderator_or_above(self) -> bool:
        """Check if user has moderator or higher privileges."""
        return self.status.value >= UserStatus.MODERATOR.value

    def can_moderate_content(self) -> bool:
        """Check if user can moderate content."""
        return self.is_moderator_or_above() and self.is_active

    def can_create_content(self) -> bool:
        """Check if user can create content."""
        return (
            self.status.value >= UserStatus.ACTIVE.value and
            self.is_active and
            not self.is_deleted
        )

    def update_last_login(self) -> None:
        """Update last login timestamp and increment counter."""
        self.last_login_at = datetime.utcnow()
        self.login_count += 1
        self.failed_login_attempts = 0  # Reset on successful login

    def increment_failed_login(self) -> None:
        """Increment failed login attempt counter."""
        self.failed_login_attempts += 1

    def should_be_locked(self, max_attempts: int = 5) -> bool:
        """Check if account should be locked due to failed attempts."""
        return self.failed_login_attempts >= max_attempts

    def reset_failed_login_attempts(self) -> None:
        """Reset failed login attempts counter."""
        self.failed_login_attempts = 0

    def __str__(self) -> str:
        return f"User(id={self.id}, email={self.email}, status={self.status.name})"
