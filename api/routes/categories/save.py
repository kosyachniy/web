"""
The creating and editing method of the category object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from libdev.lang import to_url
from consys.errors import ErrorAccess

from models.category import Category
from models.track import Track
from services.auth import sign
from services.cache import cache_categories
from lib import report


router = APIRouter()


class Type(BaseModel):
    id: int = None
    title: str = None
    description: str = None
    data: str = None
    image: str = None
    parent: int = None
    locale: str = None
    status: int = None

@router.post("/save/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Save """

    # TODO: Checking for set as a parent of yourself or children

    # No access
    if user.status < 5:
        raise ErrorAccess('save')

    # Get
    new = False
    if data.id:
        category = Category.get(data.id)

        if (user.status < 6 and category.user != user.id):
            raise ErrorAccess('save')

    else:
        category = Category(
            user=user.id,
        )
        new = True

    # Change fields
    category.title = data.title
    category.description = data.description
    category.data = data.data
    category.image = data.image
    category.parent = data.parent
    category.url = to_url(data.title)
    category.status = data.status
    if data.locale:
        category.locale = data.locale
    else:
        del category.locale

    # Checking url format
    if category.url and category.url[-1].isdigit():
        category.url += '-x'
    # Check uniq url
    if (
        not category.url
        or Category.get(id={'$ne': category.id}, url=category.url, fields={})
    ):
        category.url = str(category.created)[-6:] + '-' + (category.url or 'x')

    # Save
    category.save()

    # Cache renewal
    cache_categories()

    # Track
    Track(
        title='cat_save',
        data={
            'id': category.id,
            'title': category.title,
            'data': category.data,
            'image': category.image,
        },
        user=user.id,
        token=request.state.token,
        ip=request.state.ip,
    ).save()

    # Report
    if new:
        await report.important("Save category", {
            'category': category.id,
            'title': category.title,
            'locale': category.locale,
            'user': user.id,
        })

    # Response
    return {
        'id': category.id,
        'new': new,
        'category': category.json(),
    }
