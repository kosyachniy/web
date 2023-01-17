"""
The creating and editing method of the category object of the API
"""

from fastapi import APIRouter, Body, Request, Depends
from pydantic import BaseModel
from consys.errors import ErrorAccess

from models.category import Category
from models.track import Track
from services.auth import sign
from lib import report


router = APIRouter()


class Type(BaseModel):
    id: int = None
    title: str = None
    data: str = None
    image: str = None

@router.post("/save/")
async def handler(
    request: Request,
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Save """

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
    category.data = data.data
    category.image = data.image

    # Save
    category.save()

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
            'user': user.id,
        })

    # Response
    return {
        'id': category.id,
        'new': new,
        'category': category.json(),
    }
