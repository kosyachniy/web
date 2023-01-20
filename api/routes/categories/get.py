"""
The getting method of the category object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess, ErrorWrong

from models.category import Category
from services.auth import sign


router = APIRouter()


class Type(BaseModel):
    id: int = None
    url: str = None
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
        'locale',
        'url',
        'created',
        'updated',
    }

    # Get by url
    if data.url:
        categories = Category.get(url=data.url, fields={})
        if not categories:
            raise ErrorWrong('url')
        data.id = categories[0].id


    # Get
    categories = Category.get_tree(
        ids=data.id,
        fields=fields,
        locale=data.locale and {
            '$in': [None, data.locale],
        },  # NOTE: None → all locales
    )

    if data.id:
        categories = categories[0]

    # Response
    return {
        'categories': categories,
    }
