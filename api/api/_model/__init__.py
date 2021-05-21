import typing

from api._func import next_id
from api._func.mongodb import db


class Base:
    """ Base model """

    id: int = 0

    def __init__(self, data: dict = {}, **kwargs) -> None:
        if not data:
            data = kwargs

        for key, value in data.items():
            setattr(self, key, value)
