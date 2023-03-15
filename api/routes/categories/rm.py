"""
The removal method of the category object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.category import Category
from models.post import Post
from models.track import Track
from services.auth import sign
from services.cache import cache_categories


router = APIRouter()


class Type(BaseModel):
    id: int

@router.post("/rm/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Delete """

    # No access
    if user.status < 2:
        raise ErrorAccess('rm')

    # Get
    category = Category.get(data.id)

    if user.status < 6 and category.user != user.id:
        raise ErrorAccess('rm')

    # Reset subcategories
    for subcategory in Category.get(parent=category.id):
        del subcategory.parent
        subcategory.save()

    # Reset posts
    for post in Post.get(category=category.id):
        del post.category
        post.save()

    # Delete
    category.rm()

    # Cache renewal
    cache_categories()

    # Track
    Track(
        title='cat_rm',
        data={
            'id': data.id,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()
