"""
Category-related Pydantic schemas for content organization.

Provides comprehensive schemas for category operations:
- CRUD operations (create, update, list, view)
- Hierarchical structure (tree operations, parent-child)
- Statistics and analytics
- Admin operations (moderation, bulk operations)
"""
from typing import List, Optional, Dict, Any
from pydantic import Field, field_validator, model_validator

from app.schemas.base import BaseSchema, TimestampSchema, PaginatedResponseSchema


# Category Management Schemas

class CategoryCreateSchema(BaseSchema):
    """Schema for creating new categories."""

    name: str = Field(
        min_length=1,
        max_length=100,
        description="Category display name",
        examples=["Technology", "Programming", "Web Development"]
    )

    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        pattern=r'^[a-z0-9-]+$',
        description="URL-friendly category identifier (auto-generated if not provided)",
        examples=["technology", "programming", "web-development"]
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Category description",
        examples=["All technology-related posts and articles"]
    )

    parent_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Parent category ID for hierarchical structure",
        examples=[1, 5, 10]
    )

    icon: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Icon name or CSS class for category display",
        examples=["tech-icon", "fa-code", "laptop"]
    )

    color: Optional[str] = Field(
        default=None,
        pattern=r'^#[0-9A-Fa-f]{6}$',
        description="Category color in hex format (#RRGGBB)",
        examples=["#3B82F6", "#10B981", "#F59E0B"]
    )

    sort_order: Optional[int] = Field(
        default=0,
        ge=0,
        description="Sort order for category display",
        examples=[0, 10, 100]
    )

    meta_title: Optional[str] = Field(
        default=None,
        max_length=255,
        description="SEO meta title",
        examples=["Technology Articles and Tutorials"]
    )

    meta_description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="SEO meta description",
        examples=["Discover the latest technology trends, programming tutorials, and development insights"]
    )

    @field_validator('name')
    @classmethod
    def validate_category_name(cls, v: str) -> str:
        """Validate category name."""
        if v.strip() != v:
            raise ValueError('Category name cannot have leading/trailing whitespace')
        return v.strip()

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
        reserved_slugs = ['admin', 'api', 'www', 'blog', 'post', 'category']
        if v in reserved_slugs:
            raise ValueError('Slug is reserved')

        return v


class CategoryUpdateSchema(BaseSchema):
    """Schema for updating category information."""

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Category display name",
        examples=["Technology", "Programming"]
    )

    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        pattern=r'^[a-z0-9-]+$',
        description="URL-friendly category identifier",
        examples=["technology", "programming"]
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Category description",
        examples=["Updated category description"]
    )

    parent_id: Optional[int] = Field(
        default=None,
        gt=0,
        description="Parent category ID",
        examples=[1, 5, 10]
    )

    icon: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Icon name or CSS class",
        examples=["tech-icon", "fa-code"]
    )

    color: Optional[str] = Field(
        default=None,
        pattern=r'^#[0-9A-Fa-f]{6}$',
        description="Category color in hex format",
        examples=["#3B82F6", "#10B981"]
    )

    sort_order: Optional[int] = Field(
        default=None,
        ge=0,
        description="Sort order for display",
        examples=[0, 10, 100]
    )

    is_active: Optional[bool] = Field(
        default=None,
        description="Whether category is active and visible",
        examples=[True, False]
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

    @field_validator('name')
    @classmethod
    def validate_category_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate category name."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Category name cannot be empty')
        return v

    @field_validator('slug')
    @classmethod
    def validate_slug_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate slug format."""
        if v is not None:
            v = v.lower().strip()
            if not v:
                raise ValueError('Slug cannot be empty')
        return v


# Response Schemas

class CategoryResponseSchema(BaseSchema, TimestampSchema):
    """Schema for category information responses."""

    id: int = Field(
        description="Category ID",
        examples=[1, 5, 10]
    )

    name: str = Field(
        description="Category display name",
        examples=["Technology", "Programming"]
    )

    slug: str = Field(
        description="URL-friendly category identifier",
        examples=["technology", "programming"]
    )

    description: Optional[str] = Field(
        default=None,
        description="Category description",
        examples=["All technology-related posts"]
    )

    parent_id: Optional[int] = Field(
        default=None,
        description="Parent category ID",
        examples=[1, 5]
    )

    icon: Optional[str] = Field(
        default=None,
        description="Category icon",
        examples=["tech-icon", "fa-code"]
    )

    color: Optional[str] = Field(
        default=None,
        description="Category color in hex format",
        examples=["#3B82F6", "#10B981"]
    )

    is_active: bool = Field(
        description="Whether category is active and visible",
        examples=[True, False]
    )

    posts_count: int = Field(
        description="Number of posts in this category",
        examples=[0, 15, 42]
    )

    sort_order: int = Field(
        description="Sort order for category display",
        examples=[0, 10, 100]
    )

    meta_title: Optional[str] = Field(
        default=None,
        description="SEO meta title"
    )

    meta_description: Optional[str] = Field(
        default=None,
        description="SEO meta description"
    )

    # Computed fields
    depth: Optional[int] = Field(
        default=None,
        description="Category depth level (0 for root categories)",
        examples=[0, 1, 2]
    )

    full_path: Optional[str] = Field(
        default=None,
        description="Full category path from root",
        examples=["Technology", "Technology > Programming", "Technology > Programming > Web Development"]
    )


class CategoryTreeSchema(BaseSchema):
    """Schema for hierarchical category tree responses."""

    id: int = Field(
        description="Category ID",
        examples=[1, 5, 10]
    )

    name: str = Field(
        description="Category display name",
        examples=["Technology", "Programming"]
    )

    slug: str = Field(
        description="URL-friendly category identifier",
        examples=["technology", "programming"]
    )

    description: Optional[str] = Field(
        default=None,
        description="Category description",
        examples=["All technology-related posts"]
    )

    icon: Optional[str] = Field(
        default=None,
        description="Category icon",
        examples=["tech-icon", "fa-code"]
    )

    color: Optional[str] = Field(
        default=None,
        description="Category color in hex format",
        examples=["#3B82F6", "#10B981"]
    )

    posts_count: int = Field(
        description="Number of posts in this category",
        examples=[0, 15, 42]
    )

    is_active: bool = Field(
        description="Whether category is active",
        examples=[True, False]
    )

    depth: int = Field(
        description="Category depth level",
        examples=[0, 1, 2]
    )

    full_path: str = Field(
        description="Full category path from root",
        examples=["Technology", "Technology > Programming"]
    )

    children: List["CategoryTreeSchema"] = Field(
        default=[],
        description="Child categories"
    )

    sort_order: int = Field(
        description="Sort order for category display",
        examples=[0, 10, 100]
    )


class CategoryStatsSchema(BaseSchema):
    """Schema for detailed category statistics."""

    id: int = Field(
        description="Category ID",
        examples=[1, 5, 10]
    )

    name: str = Field(
        description="Category name",
        examples=["Technology", "Programming"]
    )

    posts_count: int = Field(
        description="Total posts in category",
        examples=[15, 42, 100]
    )

    published_posts_count: int = Field(
        description="Published posts count",
        examples=[12, 38, 95]
    )

    draft_posts_count: int = Field(
        description="Draft posts count",
        examples=[3, 4, 5]
    )

    total_views: int = Field(
        description="Total views across all posts",
        examples=[1500, 5000, 15000]
    )

    total_likes: int = Field(
        description="Total likes across all posts",
        examples=[150, 500, 1200]
    )

    total_comments: int = Field(
        description="Total comments across all posts",
        examples=[75, 250, 800]
    )

    avg_views_per_post: float = Field(
        description="Average views per post",
        examples=[35.7, 119.0, 157.9]
    )

    avg_likes_per_post: float = Field(
        description="Average likes per post",
        examples=[3.6, 11.9, 12.6]
    )

    last_post_date: Optional[str] = Field(
        default=None,
        description="Last post creation date (DD.MM.YYYY)",
        examples=["15.01.2024", "28.12.2023"]
    )

    most_popular_post_id: Optional[int] = Field(
        default=None,
        description="ID of most popular post in category",
        examples=[42, 123, 456]
    )

    engagement_rate: float = Field(
        description="Category engagement rate (likes + comments / views)",
        examples=[0.15, 0.25, 0.35]
    )


class CategoryBulkActionSchema(BaseSchema):
    """Schema for bulk category operations."""

    category_ids: List[int] = Field(
        min_items=1,
        max_items=50,
        description="List of category IDs to perform action on",
        examples=[[1, 2, 3], [5, 10, 15]]
    )

    action: str = Field(
        pattern="^(activate|deactivate|delete)$",
        description="Bulk action to perform",
        examples=["activate", "deactivate", "delete"]
    )

    reason: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Reason for bulk action",
        examples=["Cleanup inactive categories", "Reorganization"]
    )


# Filter Schemas

class CategoryFilterSchema(BaseSchema):
    """Schema for filtering categories in list endpoints."""

    parent_id: Optional[int] = Field(
        default=None,
        description="Filter by parent category ID (null for root categories)",
        examples=[1, 5, None]
    )

    is_active: Optional[bool] = Field(
        default=None,
        description="Filter by active status",
        examples=[True, False]
    )

    search: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Search in category names and descriptions",
        examples=["tech", "programming", "web"]
    )

    has_posts: Optional[bool] = Field(
        default=None,
        description="Filter categories that have posts",
        examples=[True, False]
    )

    include_stats: bool = Field(
        default=False,
        description="Include post count statistics",
        examples=[True, False]
    )

    depth_level: Optional[int] = Field(
        default=None,
        ge=0,
        le=5,
        description="Filter by category depth level",
        examples=[0, 1, 2]
    )


# List Response Schemas

class CategoryListResponseSchema(PaginatedResponseSchema[CategoryResponseSchema]):
    """Schema for paginated category list responses."""
    pass


class CategoryTreeListResponseSchema(BaseSchema):
    """Schema for category tree responses (non-paginated)."""

    categories: List[CategoryTreeSchema] = Field(
        description="Hierarchical list of categories"
    )

    total_categories: int = Field(
        description="Total number of categories",
        examples=[10, 25, 100]
    )

    root_categories_count: int = Field(
        description="Number of root categories",
        examples=[3, 5, 8]
    )

    max_depth: int = Field(
        description="Maximum depth level in tree",
        examples=[1, 2, 3]
    )