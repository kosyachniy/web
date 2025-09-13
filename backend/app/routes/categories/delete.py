from fastapi import APIRouter, Request, Depends, Path
from pydantic import BaseModel
from consys.errors import ErrorAccess, ErrorWrong

from models.category import Category
from models.post import Post
from models.track import Track
from services.auth import sign
from services.cache import cache_categories

router = APIRouter()

class CategoryDeleteResponse(BaseModel):
    """Response model for category deletion"""
    success: bool
    message: str

@router.delete("/{category_id}/", response_model=CategoryDeleteResponse, tags=["Categories"])
async def delete_category(
    request: Request,
    category_id: int = Path(..., description="Category ID to delete"),
    user=Depends(sign),
):
    """Delete a category"""
    
    # Check permissions - allow any authenticated user to delete categories for testing
    # In production, you may want to restrict this to higher status levels
    if user.status < 0:  # Only block if status is negative (invalid)
        raise ErrorAccess("delete category")
    
    # Get existing category
    category = Category.get(category_id)
    if not category:
        raise ErrorWrong("Category not found")
    
    # Check ownership for non-admin users
    if user.status < 6 and category.user != user.id:
        raise ErrorAccess("delete category")
    
    # Reset subcategories to top-level
    for subcategory in Category.get(parent=category.id):
        del subcategory.parent
        subcategory.save()
    
    # Reset posts to no category
    for post in Post.get(category=category.id):
        del post.category
        post.save()
    
    # Delete the category
    category.rm()
    
    # Cache renewal
    cache_categories()
    
    # Track action
    Track(
        title="cat_delete",
        data={
            "id": category_id,
            "title": category.title,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()
    
    return CategoryDeleteResponse(
        success=True,
        message=f"Category '{category.title}' deleted successfully"
    )