"""User domain model and related database tables."""

from __future__ import annotations

import enum
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Index, LargeBinary, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AuthProvider(enum.StrEnum):
    PASSWORD = "password"
    GOOGLE = "google"
    GITHUB = "github"
    APPLE = "apple"
    TELEGRAM = "telegram"
    PHONE = "phone"


class UserRole(enum.StrEnum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    EDITOR = "editor"
    CREATOR = "creator"
    USER = "user"
    RESTRICTED = "restricted"


class UserStatus(enum.StrEnum):
    ACTIVE = "active"
    PENDING = "pending"
    BLOCKED = "blocked"
    DELETED = "deleted"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str | None] = mapped_column(String(320), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32), unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)

    hashed_password: Mapped[str | None] = mapped_column(Text, nullable=True)
    password_salt: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)

    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_phone_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    profile: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)

    # relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all,delete-orphan")

    __table_args__ = (
        Index("ix_users_email_phone", "email", "phone"),
    )


class UserLoginActivity(Base):
    __tablename__ = "user_login_activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    provider: Mapped[AuthProvider] = mapped_column(Enum(AuthProvider), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    user: Mapped["User"] = relationship(backref="login_activities")


from app.models.post import Post  # noqa: E402  circular dependency fix
