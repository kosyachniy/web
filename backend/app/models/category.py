"""
Category model for hierarchical content organization.

Represents categories and subcategories for organizing posts and other content.
Supports hierarchical structure with parent-child relationships and tree operations.
"""
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Category(BaseModel):
    """
    Category model with hierarchical structure support.

    Provides content organization with:
    - Hierarchical parent-child relationships
    - Customizable appearance (icon, color)
    - URL-friendly slugs
    - Post count tracking
    - Status management
    """

    __tablename__ = "categories"

    # Primary identification
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Category Information
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Category display name"
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        doc="URL-friendly category identifier"
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Category description"
    )

    # Hierarchical Structure
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        doc="Parent category ID for hierarchical structure"
    )

    # Appearance and UI
    icon: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Icon name or CSS class for category display"
    )

    color: Mapped[Optional[str]] = mapped_column(
        String(7),  # Hex color format #RRGGBB
        nullable=True,
        doc="Category color in hex format (#RRGGBB)"
    )

    # Status and Visibility
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        doc="Whether category is active and visible"
    )

    # Content Statistics (denormalized for performance)
    posts_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of posts in this category"
    )

    # Display Order
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Sort order for category display"
    )

    # SEO and Metadata
    meta_title: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="SEO meta title"
    )

    meta_description: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="SEO meta description"
    )

    # Relationships
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
        lazy="select"
    )

    children: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent",
        lazy="select",
        cascade="all, delete-orphan"
    )

    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="category",
        lazy="select"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_categories_parent_active", "parent_id", "is_active"),
        Index("idx_categories_slug_active", "slug", "is_active"),
        Index("idx_categories_sort_order", "sort_order"),
    )

    def get_full_path(self, separator: str = " > ") -> str:
        """
        Get full category path from root to current category.

        Args:
            separator: String to separate category names in path

        Returns:
            Full category path string
        """
        path_parts = [self.name]
        current = self.parent

        while current is not None:
            path_parts.insert(0, current.name)
            current = current.parent

        return separator.join(path_parts)

    def get_depth(self) -> int:
        """
        Get category depth level (0 for root categories).

        Returns:
            Depth level of this category
        """
        depth = 0
        current = self.parent

        while current is not None:
            depth += 1
            current = current.parent

        return depth

    def is_root(self) -> bool:
        """Check if this is a root category (no parent)."""
        return self.parent_id is None

    def is_child_of(self, category: "Category") -> bool:
        """
        Check if this category is a child of given category.

        Args:
            category: Category to check against

        Returns:
            True if this category is a child of given category
        """
        current = self.parent
        while current is not None:
            if current.id == category.id:
                return True
            current = current.parent
        return False

    def get_all_children_ids(self) -> List[int]:
        """
        Get IDs of all descendant categories recursively.

        Returns:
            List of all child category IDs
        """
        child_ids = []

        def collect_children(category: "Category") -> None:
            for child in category.children:
                child_ids.append(child.id)
                collect_children(child)

        collect_children(self)
        return child_ids

    def increment_posts_count(self) -> None:
        """Increment the posts count for this category."""
        self.posts_count += 1

    def decrement_posts_count(self) -> None:
        """Decrement the posts count for this category."""
        if self.posts_count > 0:
            self.posts_count -= 1

    def generate_slug_from_name(self) -> str:
        """
        Generate URL-friendly slug from category name.

        Returns:
            Generated slug
        """
        import re

        # Convert to lowercase and replace spaces with hyphens
        slug = self.name.lower().replace(" ", "-")
        # Remove special characters
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        # Strip hyphens from ends
        slug = slug.strip('-')

        return slug or "category"

    @classmethod
    def build_tree_from_list(cls, categories: List["Category"]) -> List["Category"]:
        """
        Build hierarchical tree from flat list of categories.

        Args:
            categories: Flat list of categories

        Returns:
            List of root categories with populated children
        """
        # Create lookup dictionary
        category_dict = {cat.id: cat for cat in categories}

        # Initialize children lists
        for category in categories:
            category.children = []

        # Build tree structure
        root_categories = []
        for category in categories:
            if category.parent_id and category.parent_id in category_dict:
                parent = category_dict[category.parent_id]
                parent.children.append(category)
                category.parent = parent
            else:
                root_categories.append(category)

        return root_categories

    def to_tree_dict(self, include_children: bool = True) -> dict:
        """
        Convert category to dictionary with tree structure.

        Args:
            include_children: Whether to include children in output

        Returns:
            Dictionary representation with children
        """
        result = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "icon": self.icon,
            "color": self.color,
            "posts_count": self.posts_count,
            "is_active": self.is_active,
            "depth": self.get_depth(),
            "full_path": self.get_full_path()
        }

        if include_children:
            result["children"] = [
                child.to_tree_dict(include_children=True)
                for child in sorted(self.children, key=lambda c: c.sort_order)
            ]

        return result

    def __str__(self) -> str:
        return f"Category(id={self.id}, name={self.name}, parent_id={self.parent_id})"
