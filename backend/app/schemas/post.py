"""
Post-related Pydantic schemas for content management.

Provides comprehensive schemas for blog post operations:
- CRUD operations (create, update, list, view)
- Publication workflow (draft, publish, archive)
- Content organization (categories, tags)
- SEO optimization (meta tags, slugs)
- Engagement tracking (views, likes, comments)
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import Field, field_validator, model_validator

from app.schemas.base import BaseSchema, TimestampSchema, PaginatedResponseSchema, FilterSchema, DateRangeFilterSchema


class PostStatus(str, Enum):
    """Post publication status for API responses."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SCHEDULED = "scheduled"
    REJECTED = "rejected"


# Post Management Schemas

class PostCreateSchema(BaseSchema):
    """Schema for creating new blog posts."""

    title: str = Field(
        min_length=1,
        max_length=255,
        description="Post title",
        examples=["Getting Started with Python", "Machine Learning Basics", "Web Development in 2024"]
    )

    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r'^[a-z0-9-]+$',
        description="URL-friendly post identifier (auto-generated if not provided)",
        examples=["getting-started-with-python", "machine-learning-basics", "web-development-2024"]
    )

    content: str = Field(
        min_length=1,
        description="Post content (markdown supported)",
        examples=["# Introduction\n\nThis is a comprehensive guide..."]
    )

    excerpt: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Post excerpt or summary (auto-generated if not provided)",
        examples=["This comprehensive guide covers the fundamentals of Python programming..."]
    )

    category_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Category ID for post organization",
        examples=[1, 5, 10]
    )

    tags: Optional[List[str]] = Field(
        default=None,
        max_items=10,
        description="Post tags for organization",
        examples=[["python", "programming"], ["machine-learning", "ai", "tutorial"]]
    )

    featured_image_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="URL to featured image",
        examples=["https://example.com/images/featured.jpg"]
    )

    meta_title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="SEO meta title",
        examples=["Python Programming Guide - Learn Python Basics"]
    )

    meta_description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="SEO meta description",
        examples=["Comprehensive Python programming guide covering basics, best practices, and real-world examples"]
    )

    source_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Original source URL if reposted",
        examples=["https://original-source.com/article"]
    )

    is_published: bool = Field(
        default=False,
        description="Whether to publish immediately",
        examples=[False, True]
    )

    is_featured: bool = Field(
        default=False,
        description="Whether post should be featured",
        examples=[False, True]
    )

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate post title."""
        if v.strip() != v:
            raise ValueError('Title cannot have leading/trailing whitespace')
        return v.strip()

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate and normalize tags."""
        if v is None:
            return v

        # Remove duplicates, normalize to lowercase
        normalized_tags = []
        seen = set()
        for tag in v:
            tag = tag.lower().strip()
            if tag and tag not in seen:
                normalized_tags.append(tag)
                seen.add(tag)

        return normalized_tags or None

    @field_validator('slug')
    @classmethod
    def validate_slug_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate slug format."""
        if v is None:
            return v

        v = v.lower().strip()
        if not v:
            return None

        # Reserved slugs
        reserved_slugs = ['admin', 'api', 'www', 'feed', 'rss', 'sitemap']
        if v in reserved_slugs:
            raise ValueError('Slug is reserved')

        return v


class PostUpdateSchema(BaseSchema):
    """Schema for updating blog posts."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Post title",
        examples=["Updated Post Title"]
    )

    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        pattern=r'^[a-z0-9-]+$',
        description="URL-friendly post identifier",
        examples=["updated-post-slug"]
    )

    content: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Post content (markdown supported)",
        examples=["# Updated Content\n\nThis post has been updated..."]
    )

    excerpt: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Post excerpt or summary",
        examples=["Updated excerpt for the post..."]
    )

    category_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Category ID",
        examples=[1, 5, 10]
    )

    tags: Optional[List[str]] = Field(
        default=None,
        max_items=10,
        description="Post tags",
        examples=[["python", "programming", "tutorial"]]
    )

    featured_image_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="URL to featured image"
    )

    meta_title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="SEO meta title"
    )

    meta_description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="SEO meta description"
    )

    source_url: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Original source URL"
    )

    is_published: Optional[bool] = Field(
        default=None,
        description="Publication status"
    )

    is_featured: Optional[bool] = Field(
        default=None,
        description="Featured status"
    )

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate post title."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Title cannot be empty')
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate and normalize tags."""
        if v is None:
            return v

        normalized_tags = []
        seen = set()
        for tag in v:
            tag = tag.lower().strip()
            if tag and tag not in seen:
                normalized_tags.append(tag)
                seen.add(tag)

        return normalized_tags or None


# Response Schemas

class AuthorResponseSchema(BaseSchema):
    """Schema for post author information."""

    id: int = Field(
        description="Author user ID",
        examples=[1, 42, 123]
    )

    full_name: str = Field(
        description="Author's full name",
        examples=["John Doe", "Jane Smith"]
    )

    username: Optional[str] = Field(
        default=None,
        description="Author's username",
        examples=["john_doe", "jane_smith"]
    )

    avatar_url: Optional[str] = Field(
        default=None,
        description="Author's avatar image URL",
        examples=["https://example.com/avatar.jpg"]
    )

    bio: Optional[str] = Field(
        default=None,
        description="Author's bio",
        examples=["Software developer and tech writer"]
    )


class CategoryResponseSchema(BaseSchema):
    """Schema for post category information."""

    id: int = Field(
        description="Category ID",
        examples=[1, 5, 10]
    )

    name: str = Field(
        description="Category name",
        examples=["Technology", "Programming"]
    )

    slug: str = Field(
        description="Category slug",
        examples=["technology", "programming"]
    )

    color: Optional[str] = Field(
        default=None,
        description="Category color",
        examples=["#3B82F6", "#10B981"]
    )


class PostResponseSchema(BaseSchema, TimestampSchema):
    """Schema for detailed post information responses."""

    id: int = Field(
        description="Post ID",
        examples=[1, 42, 123]
    )

    title: str = Field(
        description="Post title",
        examples=["Getting Started with Python"]
    )

    slug: str = Field(
        description="URL-friendly post identifier",
        examples=["getting-started-with-python"]
    )

    content: str = Field(
        description="Full post content",
        examples=["# Introduction\n\nThis comprehensive guide..."]
    )

    excerpt: Optional[str] = Field(
        default=None,
        description="Post excerpt",
        examples=["This comprehensive guide covers..."]
    )

    author: AuthorResponseSchema = Field(
        description="Post author information"
    )

    category: Optional[CategoryResponseSchema] = Field(
        default=None,
        description="Post category information"
    )

    tags: List[str] = Field(
        default=[],
        description="Post tags",
        examples=[["python", "programming"], ["tutorial", "beginner"]]
    )

    status: PostStatus = Field(
        description="Post publication status",
        examples=["draft", "published"]
    )

    is_published: bool = Field(
        description="Whether post is published",
        examples=[True, False]
    )

    is_featured: bool = Field(
        description="Whether post is featured",
        examples=[False, True]
    )

    published_at: Optional[str] = Field(
        default=None,
        description="Publication timestamp (DD.MM.YYYY HH:MM:SS)",
        examples=["15.01.2024 14:30:00"]
    )

    featured_image_url: Optional[str] = Field(
        default=None,
        description="Featured image URL",
        examples=["https://example.com/featured.jpg"]
    )

    views_count: int = Field(
        description="Number of post views",
        examples=[0, 42, 1500]
    )

    likes_count: int = Field(
        description="Number of post likes",
        examples=[0, 5, 25]
    )

    comments_count: int = Field(
        description="Number of post comments",
        examples=[0, 3, 18]
    )

    shares_count: int = Field(
        description="Number of post shares",
        examples=[0, 2, 8]
    )

    reading_time_minutes: Optional[int] = Field(
        default=None,
        description="Estimated reading time in minutes",
        examples=[3, 5, 12]
    )

    word_count: Optional[int] = Field(
        default=None,
        description="Content word count",
        examples=[500, 1200, 2500]
    )

    source_url: Optional[str] = Field(
        default=None,
        description="Original source URL",
        examples=["https://original-source.com/article"]
    )

    meta_title: Optional[str] = Field(
        default=None,
        description="SEO meta title"
    )

    meta_description: Optional[str] = Field(
        default=None,
        description="SEO meta description"
    )

    version: int = Field(
        description="Content version number",
        examples=[1, 2, 5]
    )

    # User interaction (for authenticated requests)
    is_liked_by_user: Optional[bool] = Field(
        default=None,
        description="Whether current user liked this post",
        examples=[True, False, None]
    )

    is_bookmarked_by_user: Optional[bool] = Field(
        default=None,
        description="Whether current user bookmarked this post",
        examples=[True, False, None]
    )


class PostSummarySchema(BaseSchema, TimestampSchema):
    """Schema for post summary in list responses (reduced data)."""

    id: int = Field(
        description="Post ID",
        examples=[1, 42, 123]
    )

    title: str = Field(
        description="Post title",
        examples=["Getting Started with Python"]
    )

    slug: str = Field(
        description="URL-friendly post identifier",
        examples=["getting-started-with-python"]
    )

    excerpt: str = Field(
        description="Post excerpt",
        examples=["This comprehensive guide covers..."]
    )

    author: AuthorResponseSchema = Field(
        description="Post author information"
    )

    category: Optional[CategoryResponseSchema] = Field(
        default=None,
        description="Post category information"
    )

    tags: List[str] = Field(
        default=[],
        description="Post tags",
        examples=[["python", "programming"]]
    )

    status: PostStatus = Field(
        description="Post publication status",
        examples=["draft", "published"]
    )

    is_published: bool = Field(
        description="Whether post is published",
        examples=[True, False]
    )

    is_featured: bool = Field(
        description="Whether post is featured",
        examples=[False, True]
    )

    published_at: Optional[str] = Field(
        default=None,
        description="Publication timestamp",
        examples=["15.01.2024 14:30:00"]
    )

    featured_image_url: Optional[str] = Field(
        default=None,
        description="Featured image URL"
    )

    views_count: int = Field(
        description="Number of post views",
        examples=[42, 1500]
    )

    likes_count: int = Field(
        description="Number of post likes",
        examples=[5, 25]
    )

    comments_count: int = Field(
        description="Number of post comments",
        examples=[3, 18]
    )

    reading_time_minutes: Optional[int] = Field(
        default=None,
        description="Estimated reading time in minutes",
        examples=[5, 12]
    )

    # User interaction (for authenticated requests)
    is_liked_by_user: Optional[bool] = Field(
        default=None,
        description="Whether current user liked this post"
    )


# Filter Schemas

class PostFilterSchema(FilterSchema, DateRangeFilterSchema):
    """Schema for filtering posts in list endpoints."""

    category_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Filter by category ID",
        examples=[1, 5, 10]
    )

    author_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Filter by author ID",
        examples=[1, 42, 123]
    )

    tag: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Filter by tag",
        examples=["python", "tutorial", "beginner"]
    )

    status: Optional[PostStatus] = Field(
        default=None,
        description="Filter by publication status",
        examples=["draft", "published"]
    )

    is_published: Optional[bool] = Field(
        default=None,
        description="Filter by publication status",
        examples=[True, False]
    )

    is_featured: Optional[bool] = Field(
        default=None,
        description="Filter by featured status",
        examples=[True, False]
    )

    min_views: Optional[int] = Field(
        default=None,
        ge=0,
        description="Minimum views count",
        examples=[100, 1000, 5000]
    )

    min_likes: Optional[int] = Field(
        default=None,
        ge=0,
        description="Minimum likes count",
        examples=[10, 50, 100]
    )

    has_featured_image: Optional[bool] = Field(
        default=None,
        description="Filter posts with featured images",
        examples=[True, False]
    )


# Action Schemas

class PostModerationSchema(BaseSchema):
    """Schema for post moderation actions."""

    action: str = Field(
        pattern="^(publish|unpublish|feature|unfeature|archive|restore|delete)$",
        description="Moderation action to perform",
        examples=["publish", "feature", "archive"]
    )

    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Reason for moderation action",
        examples=["Quality content - approved for publication"]
    )


class PostLikeSchema(BaseSchema):
    """Schema for post like/unlike responses."""

    action: str = Field(
        description="Action performed (liked/unliked)",
        examples=["liked", "unliked"]
    )

    likes_count: int = Field(
        description="Updated likes count",
        examples=[6, 24]
    )

    is_liked_by_user: bool = Field(
        description="Whether user now likes the post",
        examples=[True, False]
    )


class PostBulkActionSchema(BaseSchema):
    """Schema for bulk post operations."""

    post_ids: List[int] = Field(
        min_items=1,
        max_items=50,
        description="List of post IDs to perform action on",
        examples=[[1, 2, 3], [42, 123, 456]]
    )

    action: str = Field(
        pattern="^(publish|unpublish|feature|unfeature|archive|delete)$",
        description="Bulk action to perform",
        examples=["publish", "archive", "delete"]
    )

    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Reason for bulk action",
        examples=["Bulk publication of approved content"]
    )


# List Response Schemas

class PostListResponseSchema(PaginatedResponseSchema[PostSummarySchema]):
    """Schema for paginated post list responses."""
    pass


class PostDetailListResponseSchema(PaginatedResponseSchema[PostResponseSchema]):
    """Schema for paginated detailed post list responses."""
    pass


# Statistics Schemas

class PostStatsSchema(BaseSchema):
    """Schema for post statistics."""

    total_posts: int = Field(
        description="Total number of posts",
        examples=[150, 500, 1000]
    )

    published_posts: int = Field(
        description="Number of published posts",
        examples=[120, 450, 900]
    )

    draft_posts: int = Field(
        description="Number of draft posts",
        examples=[25, 40, 80]
    )

    featured_posts: int = Field(
        description="Number of featured posts",
        examples=[5, 15, 25]
    )

    total_views: int = Field(
        description="Total views across all posts",
        examples=[15000, 50000, 100000]
    )

    total_likes: int = Field(
        description="Total likes across all posts",
        examples=[750, 2500, 5000]
    )

    total_comments: int = Field(
        description="Total comments across all posts",
        examples=[300, 1200, 2500]
    )

    avg_views_per_post: float = Field(
        description="Average views per post",
        examples=[100.0, 111.1, 100.0]
    )

    avg_likes_per_post: float = Field(
        description="Average likes per post",
        examples=[5.0, 5.6, 5.0]
    )

    most_viewed_post_id: Optional[int] = Field(
        default=None,
        description="ID of most viewed post",
        examples=[42, 123, 456]
    )

    most_liked_post_id: Optional[int] = Field(
        default=None,
        description="ID of most liked post",
        examples=[42, 123, 456]
    )

    posts_published_today: int = Field(
        description="Posts published today",
        examples=[0, 2, 5]
    )

    posts_published_this_week: int = Field(
        description="Posts published this week",
        examples=[5, 15, 25]
    )

    posts_published_this_month: int = Field(
        description="Posts published this month",
        examples=[20, 60, 100]
    )