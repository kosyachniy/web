"""
Post model for blog posts and content management.

Represents blog posts with full content management features including:
- Rich content with markdown support
- Category and tag organization
- Publication workflow with drafts
- SEO optimization with slugs and meta
- Engagement tracking (views, likes)
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, SoftDeleteMixin


class PostStatus(Enum):
    """Post publication status."""
    DRAFT = 0        # Draft - not visible to public
    PUBLISHED = 1    # Published - visible to public
    ARCHIVED = 2     # Archived - not visible but preserved
    SCHEDULED = 3    # Scheduled for future publication
    REJECTED = 4     # Rejected by moderators


class Post(BaseModel, SoftDeleteMixin):
    """
    Post model with comprehensive content management features.

    Provides content publishing with:
    - Rich text content with markdown support
    - Category and tag organization
    - Publication workflow and status management
    - SEO optimization with slugs and metadata
    - Engagement tracking (views, likes, comments)
    - Content versioning support
    """

    __tablename__ = "posts"

    # Primary identification
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Content
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Post title"
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="URL-friendly post identifier"
    )

    excerpt: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Post excerpt or summary"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Full post content (markdown supported)"
    )

    # Content Organization
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Category ID for post organization"
    )

    tags: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        doc="Post tags as JSON array"
    )

    # Publication Management
    status: Mapped[PostStatus] = mapped_column(
        Integer,  # We'll store as integer for backward compatibility
        default=PostStatus.DRAFT.value,
        nullable=False,
        index=True,
        doc="Post publication status"
    )

    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Whether post is published and visible"
    )

    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        doc="Whether post is featured"
    )

    published_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        doc="Publication timestamp"
    )

    # Author Information
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Post author user ID"
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

    # Media
    featured_image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="Featured image URL"
    )

    # Engagement Metrics (denormalized for performance)
    views_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True,
        doc="Number of post views"
    )

    likes_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of post likes"
    )

    comments_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of post comments"
    )

    shares_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of post shares"
    )

    # Content Statistics
    reading_time_minutes: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Estimated reading time in minutes"
    )

    word_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="Content word count"
    )

    # External and Source Information
    source_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        doc="Original source URL if reposted"
    )

    # Versioning and History
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        doc="Content version number"
    )

    last_modified_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        doc="User who last modified the post"
    )

    # Relationships
    author: Mapped["User"] = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="posts",
        lazy="select"
    )

    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="posts",
        lazy="select"
    )

    last_modified_by_user: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[last_modified_by],
        lazy="select"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_posts_author_status", "author_id", "status"),
        Index("idx_posts_category_published", "category_id", "is_published"),
        Index("idx_posts_published_created", "is_published", "created_at"),
        Index("idx_posts_status_featured", "status", "is_featured"),
        Index("idx_posts_views_published", "views_count", "is_published"),
        Index("idx_posts_slug_active", "slug", "is_published"),
    )

    def publish(self) -> None:
        """Publish the post."""
        self.status = PostStatus.PUBLISHED.value
        self.is_published = True
        if self.published_at is None:
            self.published_at = datetime.utcnow()

    def unpublish(self) -> None:
        """Unpublish the post (make it draft)."""
        self.status = PostStatus.DRAFT.value
        self.is_published = False

    def archive(self) -> None:
        """Archive the post."""
        self.status = PostStatus.ARCHIVED.value
        self.is_published = False

    def increment_views(self) -> None:
        """Increment the views count."""
        self.views_count += 1

    def increment_likes(self) -> None:
        """Increment the likes count."""
        self.likes_count += 1

    def decrement_likes(self) -> None:
        """Decrement the likes count."""
        if self.likes_count > 0:
            self.likes_count -= 1

    def increment_comments(self) -> None:
        """Increment the comments count."""
        self.comments_count += 1

    def decrement_comments(self) -> None:
        """Decrement the comments count."""
        if self.comments_count > 0:
            self.comments_count -= 1

    def calculate_reading_time(self) -> int:
        """
        Calculate estimated reading time based on content.

        Assumes average reading speed of 200 words per minute.

        Returns:
            Estimated reading time in minutes
        """
        if not self.content:
            return 0

        # Simple word count (split by whitespace)
        word_count = len(self.content.split())
        self.word_count = word_count

        # Average reading speed: 200 words per minute
        reading_time = max(1, round(word_count / 200))
        self.reading_time_minutes = reading_time

        return reading_time

    def generate_slug_from_title(self) -> str:
        """
        Generate URL-friendly slug from post title.

        Returns:
            Generated slug
        """
        import re

        # Convert to lowercase and replace spaces with hyphens
        slug = self.title.lower().replace(" ", "-")
        # Remove special characters
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        # Remove multiple hyphens
        slug = re.sub(r'-+', '-', slug)
        # Strip hyphens from ends
        slug = slug.strip('-')

        return slug or f"post-{self.id}" if self.id else "untitled-post"

    def generate_excerpt_from_content(self, max_length: int = 200) -> str:
        """
        Generate excerpt from post content.

        Args:
            max_length: Maximum length of excerpt

        Returns:
            Generated excerpt
        """
        if not self.content:
            return ""

        # Remove markdown and HTML tags (simple approach)
        import re
        clean_content = re.sub(r'[#*_`\[\]()]+', '', self.content)
        clean_content = re.sub(r'https?://\S+', '', clean_content)

        # Get first paragraph or first N characters
        first_paragraph = clean_content.split('\n')[0].strip()
        if len(first_paragraph) <= max_length:
            return first_paragraph

        # Truncate and add ellipsis
        truncated = first_paragraph[:max_length].rsplit(' ', 1)[0]
        return f"{truncated}..."

    def get_status_display(self) -> str:
        """Get human-readable status."""
        try:
            return PostStatus(self.status).name.title()
        except ValueError:
            return "Unknown"

    def can_be_edited_by(self, user_id: int, user_is_admin: bool = False) -> bool:
        """
        Check if post can be edited by given user.

        Args:
            user_id: ID of user requesting edit
            user_is_admin: Whether user has admin privileges

        Returns:
            True if user can edit this post
        """
        return user_is_admin or self.author_id == user_id

    def __str__(self) -> str:
        return f"Post(id={self.id}, title={self.title[:50]}, status={self.get_status_display()})"
