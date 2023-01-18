"""
The getting method of the category object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.category import Category
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int | list[int] = None
    parent: int = None
    locale: str = None

@router.post("/get/")
async def handler(
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Get """

    # No access
    if user.status < 2:
        raise ErrorAccess('get')

    # Fields
    fields = {
        'id',
        'title',
        'data',
        'image',
        'parent',
        'created',
        'updated',
    }

    # Get
    categories = Category.get_tree(
        ids=data.id,
        parent=data.parent,
        fields=fields,
        locale=data.locale,  # NOTE: None → all locales
    )

    # Response
    return {
        'categories': categories,
    }
