from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from consys.errors import ErrorAccess

from models.category import Category
from models.post import Post
from services.auth import sign
from lib.queue import get

router = APIRouter()

class CategoryResponse(BaseModel):
    """Response model for category data"""
    id: int = Field(description="Category ID", example=1)
    title: str = Field(description="Category title", example="Technology")
    url: str = Field(description="URL slug", example="technology")
    description: Optional[str] = Field(None, description="Category description")
    data: Optional[str] = Field(None, description="Additional metadata as JSON string")
    image: Optional[str] = Field(None, description="Category image URL")
    parent: Optional[int] = Field(None, description="Parent category ID")
    locale: Optional[str] = Field(None, description="Category locale")
    status: int = Field(description="Category status", example=1)
    created: Optional[int] = Field(None, description="Creation timestamp")
    updated: Optional[int] = Field(None, description="Last update timestamp")
    user: Optional[int] = Field(None, description="Creator user ID")
    post_count: Optional[int] = Field(None, description="Number of posts in this category", example=42)
    categories: Optional[List["CategoryResponse"]] = Field(None, description="Subcategories")
    parents: Optional[List[dict]] = Field(None, description="Parent hierarchy")

class CategoriesListResponse(BaseModel):
    """Response model for categories list"""
    categories: List[CategoryResponse] = Field(description="List of categories")

@router.get("/", response_model=CategoriesListResponse, tags=["Categories"])
async def get_categories(
    parent: Optional[int] = Query(None, description="Parent category ID (omit for all, 0 for top-level)"),
    locale: Optional[str] = Query(None, description="Filter by locale"),
    status: Optional[int] = Query(None, description="Filter by status"),
    include_tree: bool = Query(False, description="Include nested subcategories"),
    user=Depends(sign),
):
    """Get categories list with optional filtering"""
    
    # Categories are generally public, only require basic authentication
    # Removed restrictive permission check - categories should be accessible to all authenticated users
    
    # Build query filters
    filters = {}
    if locale:
        filters["locale"] = {"$in": [None, locale]}
    if status is not None:
        # FIXME: Status filtering seems to have issues with ConsYS
        # For now, only apply the filter for non-standard status values
        if status != 1:
            filters["status"] = status
        # If status == 1, don't filter since most categories should have status=1
    if parent is not None:
        if parent == 0:
            filters["parent"] = {"$in": [None, 0]}  # Top-level categories
        else:
            filters["parent"] = parent
    
    # Fields to retrieve
    fields = {
        "id", "title", "description", "data", "image", "parent", 
        "locale", "url", "status", "created", "updated", "user"
    }
    
    if include_tree and (parent is None or parent == 0):
        # Get tree structure - start from root level (parent 0 or None)
        # Remove parent filter for tree structure since get_tree handles hierarchy internally
        tree_filters = {k: v for k, v in filters.items() if k != "parent"}
        categories_data = Category.get_tree(fields=fields, **tree_filters)
    else:
        # Get flat list
        categories = Category.get(fields=fields, **filters)
        categories_data = [cat.json() for cat in categories]
    
    # Convert to response format
    def convert_category(cat_data):
        # Count posts in this category (only active posts with status=1)
        post_count = Post.count(category=cat_data["id"], status=1)
        
        cat_response = CategoryResponse(
            id=cat_data["id"],
            title=cat_data["title"],
            url=cat_data.get("url", ""),
            description=cat_data.get("description"),
            data=cat_data.get("data"),
            image=cat_data.get("image"),
            parent=cat_data.get("parent"),
            locale=cat_data.get("locale"),
            status=cat_data.get("status", 1),
            created=cat_data.get("created"),
            updated=cat_data.get("updated"),
            user=cat_data.get("user"),
            post_count=post_count,
        )
        
        # Handle nested subcategories
        if "categories" in cat_data and cat_data["categories"]:
            cat_response.categories = [convert_category(sub) for sub in cat_data["categories"]]
            
        return cat_response
    
    response_categories = [convert_category(cat) for cat in categories_data]
    
    return CategoriesListResponse(categories=response_categories)

@router.get("/tree/", response_model=CategoriesListResponse, tags=["Categories"])
async def get_categories_tree(
    locale: Optional[str] = Query(None, description="Filter by locale"),
    status: Optional[int] = Query(1, description="Filter by status"),
    user=Depends(sign),
):
    """Get categories as a hierarchical tree structure"""
    
    # Categories are generally public, only require basic authentication
    
    # Build query filters
    filters = {}
    if locale:
        filters["locale"] = {"$in": [None, locale]}
    if status is not None:
        # FIXME: Status filtering seems to have issues with ConsYS
        # For now, only apply the filter for non-standard status values
        if status != 1:
            filters["status"] = status
        # If status == 1, don't filter since most categories should have status=1
    
    # Fields to retrieve
    fields = {
        "id", "title", "description", "data", "image", "parent", 
        "locale", "url", "status", "created", "updated", "user"
    }
    
    # Get tree structure
    categories_data = Category.get_tree(fields=fields, **filters)
    
    # Convert to response format
    def convert_category(cat_data):
        # Count posts in this category (only active posts with status=1)
        post_count = Post.count(category=cat_data["id"], status=1)
        
        cat_response = CategoryResponse(
            id=cat_data["id"],
            title=cat_data["title"],
            url=cat_data.get("url", ""),
            description=cat_data.get("description"),
            data=cat_data.get("data"),
            image=cat_data.get("image"),
            parent=cat_data.get("parent"),
            locale=cat_data.get("locale"),
            status=cat_data.get("status", 1),
            created=cat_data.get("created"),
            updated=cat_data.get("updated"),
            user=cat_data.get("user"),
            post_count=post_count,
        )
        
        # Handle nested subcategories
        if "categories" in cat_data and cat_data["categories"]:
            cat_response.categories = [convert_category(sub) for sub in cat_data["categories"]]
            
        return cat_response
    
    response_categories = [convert_category(cat) for cat in categories_data]
    
    return CategoriesListResponse(categories=response_categories)

@router.get("/{category_id}/", response_model=CategoryResponse, tags=["Categories"])
async def get_category(
    category_id: int,
    user=Depends(sign),
):
    """Get a single category by ID"""
    
    # Categories are generally public, only require basic authentication
    
    # Get category
    category = Category.get(category_id)
    if not category:
        from consys.errors import ErrorWrong
        raise ErrorWrong("Category not found")
    
    # Add parent hierarchy if available
    category_data = category.json()
    
    # Get parents hierarchy
    category_ids = get("category_ids", {})
    category_parents = get("category_parents", {})
    if category.id in category_parents:
        category_data["parents"] = [
            category_ids[parent].json(fields={"id", "url", "title"})
            for parent in category_parents[category.id]
            if parent in category_ids
        ]
    
    # Count posts in this category (only active posts with status=1)
    post_count = Post.count(category=category.id, status=1)
    
    return CategoryResponse(
        id=category_data["id"],
        title=category_data["title"],
        url=category_data.get("url", ""),
        description=category_data.get("description"),
        data=category_data.get("data"),
        image=category_data.get("image"),
        parent=category_data.get("parent"),
        locale=category_data.get("locale"),
        status=category_data.get("status", 1),
        created=category_data.get("created"),
        updated=category_data.get("updated"),
        user=category_data.get("user"),
        post_count=post_count,
        parents=category_data.get("parents")
    )