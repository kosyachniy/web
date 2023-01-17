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
        'created',
        'updated',
    }

    # Get
    # TODO: parent
    categories = Category.complex(
        ids=data.id,
        fields=fields,
        locale=data.locale,  # NOTE: None → all locales
    )

    # TODO: create tree

    # Response
    return {
        'categories': categories,
    }
