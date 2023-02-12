"""
The getting method of the category object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess, ErrorWrong

from models.category import Category
from services.auth import sign
from lib.queue import get


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
        'description',
        'data',
        'image',
        'parent',
        'locale',
        'url',
        'status',
        'created',
        'updated',
    }

    # Get by url
    if data.url:
        category = get('category_urls').get(data.url)
        if not category:
            raise ErrorWrong('url')
        data.id = category.id

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

        category_ids = get('category_ids')
        categories['parents'] = [
            category_ids[parent].json(fields={'id', 'url', 'title'})
            for parent in get('category_parents', {}).get(categories['id'], [])
            if parent in category_ids
        ]

    # Response
    return {
        'categories': categories,
    }
