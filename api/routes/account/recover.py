"""
The password recover method of the account object of the API
"""

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from consys.errors import ErrorWrong, ErrorAccess

from models.user import User, process_lower, pre_process_phone
from services.auth import sign
from lib import generate_password, report


router = APIRouter()


class Type(BaseModel):
    login: str

@router.post("/recover/")
async def handler(
    data: Type = Body(...),
    user = Depends(sign),
):
    """ Recover password """

    # No access
    if user.status < 2:
        raise ErrorAccess('recover')

    # Get

    new = False
    login = process_lower(data.login)
    users = User.get(login=login, fields={})

    if users:
        user = users[0]
    else:
        new = True

    if new:
        mail = process_lower(data.login)
        users = User.get(mail=mail, fields={})

        if users:
            user = users[0]
            new = False

    if new:
        phone = pre_process_phone(data.login)
        users = User.get(phone=phone, fields={})

        if users:
            user = users[0]
            new = False

    if new:
        raise ErrorWrong('login')

    # Update password
    password = generate_password()
    user.password = password
    user.save()

    # Send
    # TODO: send by mail
    # TODO: send by SMS

    # Report
    await report.request("Recover password", {
        'password': password,
        'user': user.id,
    })
