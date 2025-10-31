"""
Base SQLAlchemy Model

Base model with common fields and configurations.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    # Generate table names automatically from class names
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Convert CamelCase to snake_case
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class TimestampedMixin:
    """Mixin for models that need timestamp tracking."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Record creation timestamp"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Record last update timestamp"
    )


class BaseModel(Base, TimestampedMixin):
    """
    Base model with ID and timestamps.

    Provides:
    - UUID primary key
    - Created/updated timestamps
    - Common configuration
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        doc="Unique identifier"
    )

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """
        Convert model to dictionary.

        Args:
            exclude: Set of field names to exclude

        Returns:
            Dictionary representation
        """
        exclude = exclude or set()
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }

    def update_from_dict(self, data: dict[str, Any]) -> None:
        """
        Update model from dictionary.

        Args:
            data: Dictionary with field values
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
