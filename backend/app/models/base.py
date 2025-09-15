"""
Base model class with common fields and utilities.

Provides standard fields and methods that all database models inherit:
- Primary key management
- Timestamp fields (created_at, updated_at)
- Soft delete support
- Model utilities and mixins
"""
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class TimestampMixin:
    """
    Mixin for timestamp fields that are common to most models.

    Provides created_at and updated_at fields with automatic management.
    """

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


class SoftDeleteMixin:
    """
    Mixin for soft delete functionality.

    Provides is_deleted field and related methods for soft deletion
    instead of hard deletion from database.
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Soft delete flag"
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Soft delete timestamp"
    )

    def soft_delete(self) -> None:
        """Mark record as deleted without removing from database."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        """Restore soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None


class BaseModel(Base, TimestampMixin):
    """
    Abstract base model class for all database entities.

    Provides:
    - Primary key management
    - Timestamp fields (created_at, updated_at)
    - Common utility methods
    - Consistent table configuration
    """

    __abstract__ = True  # Don't create table for this class

    def to_dict(self, exclude: set[str] | None = None) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.

        Args:
            exclude: Set of field names to exclude from result

        Returns:
            Dictionary representation of model
        """
        exclude = exclude or set()

        result = {}
        for column in self.__table__.columns:
            field_name = column.name
            if field_name not in exclude:
                value = getattr(self, field_name)
                # Convert datetime to ISO format string
                if isinstance(value, datetime):
                    value = value.isoformat()
                result[field_name] = value

        return result

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update model instance from dictionary.

        Args:
            data: Dictionary with field values to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        """String representation of model instance."""
        class_name = self.__class__.__name__

        # Try to use 'id' field if available
        if hasattr(self, 'id'):
            return f"<{class_name}(id={self.id})>"

        # Fallback to generic representation
        return f"<{class_name}()>"


class ActiveRecordMixin:
    """
    Mixin providing active record pattern methods.

    Note: These methods require a session to be passed in.
    For repository pattern, use dedicated repository classes.
    """

    @classmethod
    def create(cls, session, **kwargs):
        """
        Create and save new instance.

        Args:
            session: Database session
            **kwargs: Field values for new instance

        Returns:
            Created instance
        """
        instance = cls(**kwargs)
        session.add(instance)
        session.flush()  # Get the ID without committing
        return instance

    def save(self, session) -> None:
        """
        Save current instance to database.

        Args:
            session: Database session
        """
        session.add(self)
        session.flush()

    def delete(self, session) -> None:
        """
        Delete current instance from database.

        Args:
            session: Database session
        """
        session.delete(self)
        session.flush()