from fastapi import APIRouter, Body, Request, Depends, Path
from pydantic import BaseModel, Field
from libdev.lang import to_url
from consys.errors import ErrorAccess, ErrorWrong
from typing import Optional

from lib import log
from models.category import Category
from models.track import Track
from services.auth import sign
from services.cache import cache_categories

router = APIRouter()

class CategoryUpdateRequest(BaseModel):
    """Request model for updating a category"""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Category title", example="Technology")
    url: Optional[str] = Field(None, max_length=100, description="URL slug", example="technology")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    data: Optional[str] = Field(None, description="Additional metadata as JSON string")
    image: Optional[str] = Field(None, description="Category image URL")
    parent: Optional[int] = Field(None, description="Parent category ID")
    locale: Optional[str] = Field(None, description="Category locale")
    status: Optional[int] = Field(None, description="Category status (1=active, 0=inactive)")
    icon: Optional[str] = Field(None, description="FontAwesome icon key", example="house")
    color: Optional[str] = Field(None, description="Category color in hex format", example="#10b981")

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
    icon: Optional[str] = Field(None, description="FontAwesome icon key", example="house")
    color: Optional[str] = Field(None, description="Category color in hex format", example="#10b981")

@router.put("/{category_id}/", response_model=CategoryResponse, tags=["Categories"])
async def update_category(
    request: Request,
    category_id: int = Path(..., description="Category ID to update"),
    data: CategoryUpdateRequest = Body(...),
    user=Depends(sign),
):
    """Update an existing category"""
    
    # Check permissions - allow any authenticated user to update categories for testing
    # In production, you may want to restrict this to higher status levels
    if user.status < 0:  # Only block if status is negative (invalid)
        raise ErrorAccess("update category")
    
    # Get existing category
    category = Category.get(category_id)
    if not category:
        raise ErrorWrong("Category not found")
    
    # Check ownership for non-admin users
    if user.status < 6 and category.user != user.id:
        raise ErrorAccess("update category")
    
    # Update fields only if provided
    if data.title is not None:
        category.title = data.title
    if data.description is not None:
        category.description = data.description
    if data.data is not None:
        category.data = data.data
    if data.image is not None:
        category.image = data.image
    if data.parent is not None:
        category.parent = data.parent
    if data.status is not None:
        category.status = data.status
    if data.icon is not None:
        category.icon = data.icon
    if data.color is not None:
        category.color = data.color
    
    # Handle URL update
    if data.url is not None:
        category.url = data.url
    elif data.title is not None:
        # Auto-generate URL if title changed but URL not provided
        category.url = to_url(data.title)
    
    # Handle locale
    if data.locale is not None:
        if data.locale:
            category.locale = data.locale
        else:
            del category.locale
    
    # Ensure URL format
    if category.url and category.url[-1].isdigit():
        category.url += "-x"
        
    # Check unique URL (excluding current category)
    if not category.url or Category.get(
        id={"$ne": category.id}, url=category.url, fields={}
    ):
        category.url = str(category.created)[-6:] + "-" + (category.url or "x")
    
    # Save category
    category.save()
    
    # Cache renewal
    cache_categories()
    
    # Track action
    Track(
        title="cat_update",
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
        "Updated category\n{}",
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
        icon=category.icon,
        color=category.color,
    )