"""
Categories API Endpoints

Layer 6: HTTP Interface - Category management endpoints.
Minimal implementation to get frontend working.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/categories", tags=["Categories"])


# Response schemas
class CategoryResponse(BaseModel):
    """Single category response."""
    id: int
    url: str
    title: str
    description: Optional[str] = None
    parent: Optional[int] = 0
    status: int = 1
    locale: str = "en"
    created: Optional[int] = None
    updated: Optional[int] = None
    categories: list["CategoryResponse"] = Field(default_factory=list)  # Nested subcategories

    class Config:
        from_attributes = True


# Update forward references
CategoryResponse.model_rebuild()


class CategoriesListResponse(BaseModel):
    """List of categories response."""
    categories: list[CategoryResponse]


# Mock data for development
MOCK_CATEGORIES = [
    {
        "id": 1,
        "url": "technology",
        "title": "Technology",
        "description": "Latest tech news and trends",
        "parent": 0,
        "status": 1,
        "locale": "en",
        "categories": []
    },
    {
        "id": 2,
        "url": "business",
        "title": "Business",
        "description": "Business insights and analysis",
        "parent": 0,
        "status": 1,
        "locale": "en",
        "categories": []
    },
    {
        "id": 3,
        "url": "lifestyle",
        "title": "Lifestyle",
        "description": "Lifestyle and culture content",
        "parent": 0,
        "status": 1,
        "locale": "en",
        "categories": []
    }
]


@router.get(
    "/",
    response_model=CategoriesListResponse,
    summary="Get categories",
    description="Get list of categories with optional filtering by parent, locale, and status."
)
async def get_categories(
    parent: Optional[int] = Query(None, description="Parent category ID (0 for top-level)"),
    locale: Optional[str] = Query(None, description="Locale filter"),
    status: Optional[int] = Query(None, description="Status filter (1 = active)"),
    include_tree: bool = Query(False, description="Include subcategories tree")
) -> CategoriesListResponse:
    """
    Get categories with optional filtering.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    # Filter mock data based on parameters
    filtered_categories = MOCK_CATEGORIES.copy()

    # Filter by parent if specified
    if parent is not None:
        filtered_categories = [cat for cat in filtered_categories if cat.get("parent") == parent]

    # Filter by locale if specified
    if locale is not None:
        # For now, return all categories regardless of locale
        # In production, filter by locale
        pass

    # Filter by status if specified
    if status is not None:
        filtered_categories = [cat for cat in filtered_categories if cat.get("status") == status]

    return CategoriesListResponse(
        categories=[CategoryResponse(**cat) for cat in filtered_categories]
    )


@router.get(
    "/tree/",
    response_model=CategoriesListResponse,
    summary="Get category tree",
    description="Get hierarchical category tree structure."
)
async def get_category_tree() -> CategoriesListResponse:
    """
    Get complete category tree with nested subcategories.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    return CategoriesListResponse(
        categories=[CategoryResponse(**cat) for cat in MOCK_CATEGORIES]
    )


@router.get(
    "/{category_id}/",
    response_model=CategoryResponse,
    summary="Get category by ID",
    description="Get a single category by its ID."
)
async def get_category(category_id: int) -> CategoryResponse:
    """
    Get a category by ID.

    Currently returns mock data for development.
    TODO: Implement real database queries once migrations are applied.
    """
    # Find category in mock data
    category = next((cat for cat in MOCK_CATEGORIES if cat["id"] == category_id), None)

    if not category:
        # Return empty category with just ID
        return CategoryResponse(
            id=category_id,
            url=f"category-{category_id}",
            title=f"Category {category_id}",
            description=None,
            parent=0,
            status=1,
            locale="en",
            categories=[]
        )

    return CategoryResponse(**category)
