"""
User authorization
"""

from fastapi import Body
from pydantic import BaseModel

from routes.account.online import get_user


class Type(BaseModel):
    token: str

def auth(data: Type = Body(...)):
    user, _ = get_user(data.token)
    return user

def get_token(data: Type = Body(...)):
    _, token = get_user(data.token)
    return token
