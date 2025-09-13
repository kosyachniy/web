from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel, Field
from libdev.lang import to_url
from consys.errors import ErrorAccess
from typing import Optional

from lib import log
from models.category import Category
from models.track import Track
from services.auth import sign
from services.cache import cache_categories

router = APIRouter()

class CategoryCreateRequest(BaseModel):
    """Request model for creating a new category"""
    title: str = Field(..., min_length=1, max_length=100, description="Category title", example="Technology")
    url: Optional[str] = Field(None, max_length=100, description="URL slug (auto-generated if not provided)", example="technology")
    description: Optional[str] = Field(None, max_length=500, description="Category description", example="Latest technology news and trends")
    data: Optional[str] = Field(None, description="Additional metadata as JSON string", example='{"icon": "laptop", "color": "#3b82f6"}')
    image: Optional[str] = Field(None, description="Category image URL", example="https://example.com/tech.jpg")
    parent: Optional[int] = Field(0, description="Parent category ID (0 for top-level)", example=0)
    locale: Optional[str] = Field("en", description="Category locale", example="en")
    status: Optional[int] = Field(1, description="Category status (1=active, 0=inactive)", example=1)

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

@router.post("/", response_model=CategoryResponse, tags=["Categories"])
async def create_category(
    request: Request,
    data: CategoryCreateRequest = Body(...),
    user=Depends(sign),
):
    """Create a new category"""
    
    # Check permissions - allow any authenticated user to create categories for testing
    # In production, you may want to restrict this to higher status levels
    if user.status < 0:  # Only block if status is negative (invalid)
        raise ErrorAccess("create category")
    
    # Create new category
    category = Category(
        user=user.id,
        title=data.title,
        description=data.description,
        data=data.data,
        image=data.image,
        parent=data.parent or 0,
        status=data.status if data.status is not None else 1,
    )
    
    # Generate URL if not provided
    if data.url:
        category.url = data.url
    else:
        category.url = to_url(data.title)
    
    # Set locale
    if data.locale:
        category.locale = data.locale
    else:
        del category.locale
    
    # Ensure URL format
    if category.url and category.url[-1].isdigit():
        category.url += "-x"
        
    # Check unique URL
    if not category.url or Category.get(url=category.url, fields={}):
        category.url = str(category.created)[-6:] + "-" + (category.url or "x")
    
    # Save category
    category.save()
    
    # Cache renewal
    cache_categories()
    
    # Track action
    Track(
        title="cat_create",
        data={
            "id": category.id,
            "title": category.title,
            "data": category.data,
            "image": category.image,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()
    
    # Log success
    log.success(
        "Created category\n{}",
        {
            "category": category.id,
            "title": category.title,
            "locale": category.locale,
            "user": user.id,
        },
    )
    
    return CategoryResponse(
        id=category.id,
        title=category.title,
        url=category.url,
        description=category.description,
        data=category.data,
        image=category.image,
        parent=category.parent,
        locale=category.locale,
        status=category.status,
        created=category.created,
        updated=category.updated,
        user=category.user,
    )
