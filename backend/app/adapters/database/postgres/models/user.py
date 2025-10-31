"""
User SQLAlchemy Model

PostgreSQL User table model with all fields and constraints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, Index, ARRAY, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY

from .base import BaseModel


class User(BaseModel):
    """
    User SQLAlchemy model for PostgreSQL.

    Maps to the users table with all user fields,
    constraints, and database-specific optimizations.
    """

    __tablename__ = "users"

    # Basic Information
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="User email address"
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique username"
    )

    full_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="User full name"
    )

    # Authentication
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Hashed password"
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Email verification status"
    )

    email_verification_token: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        doc="Email verification token"
    )

    # Status and Permissions
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending_verification",
        nullable=False,
        index=True,
        doc="User status"
    )

    roles: Mapped[list[str]] = mapped_column(
        PG_ARRAY(String(50)),
        default=["user"],
        nullable=False,
        doc="User roles (multiple roles supported)"
    )

    # Activity Tracking
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last login timestamp"
    )

    login_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Total login count"
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Failed login attempts"
    )

    locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Account lock expiration"
    )

    # Preferences
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="UTC",
        nullable=False,
        doc="User timezone"
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False,
        doc="Preferred language"
    )

    # Additional indexes for performance
    __table_args__ = (
        # Composite index for authentication queries
        Index("idx_users_email_status", "email", "status"),
        Index("idx_users_username_status", "username", "status"),

        # GIN index for roles array queries
        Index("idx_users_roles", "roles", postgresql_using="gin"),

        # Index for activity tracking
        Index("idx_users_last_login", "last_login_at"),

        # Index for locked accounts cleanup
        Index("idx_users_locked_until", "locked_until"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    def to_domain_entity(self) -> "app.domain.entities.User":
        """
        Convert SQLAlchemy model to domain entity.

        Returns:
            Domain User entity
        """
        from app.domain.entities import User as DomainUser, UserStatus, UserRole

        return DomainUser(
            id=self.id,
            email=self.email,
            username=self.username,
            full_name=self.full_name,
            password_hash=self.password_hash,
            is_email_verified=self.is_email_verified,
            email_verification_token=self.email_verification_token,
            status=UserStatus(self.status),
            roles=[UserRole(role) for role in self.roles],
            last_login_at=self.last_login_at,
            login_count=self.login_count,
            failed_login_attempts=self.failed_login_attempts,
            locked_until=self.locked_until,
            timezone=self.timezone,
            language=self.language,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain_entity(cls, user: "app.domain.entities.User") -> User:
        """
        Create SQLAlchemy model from domain entity.

        Args:
            user: Domain User entity

        Returns:
            SQLAlchemy User model
        """
        return cls(
            id=user.id,
            email=str(user.email),
            username=user.username,
            full_name=user.full_name,
            password_hash=user.password_hash,
            is_email_verified=user.is_email_verified,
            email_verification_token=user.email_verification_token,
            status=user.status.value,
            roles=[role.value for role in user.roles],
            last_login_at=user.last_login_at,
            login_count=user.login_count,
            failed_login_attempts=user.failed_login_attempts,
            locked_until=user.locked_until,
            timezone=user.timezone,
            language=user.language,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
