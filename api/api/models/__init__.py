"""
Base model of DB object
"""

import typing

from ..funcs import next_id
from ..funcs.mongodb import db


class Attribute:
    """ Descriptor """

    name: str = None
    types: typing.Any = None
    default: typing.Any = None

    def __init__(self, types, default=None):
        self.types = types
        self.default = default

    def __set_name__(self, instance, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value) -> None:
        instance.__dict__[self.name] = value

class Base:
    """ Base model """

    id = Attribute(int, 0)

    def __init__(self, data: dict = {}, **kwargs) -> None:
        if not data:
            data = kwargs

        for name, value in data.items():
            setattr(self, name, value)

    @classmethod
    def get(
        cls,
        ids: typing.Union[typing.List[int], int, None] = None,
        *,
        fields: typing.Optional[typing.List[str]] = None,
        search: typing.Optional[str] = None,
        count: typing.Optional[int] = None,
        offset: int = 0,
        **kw,
    ) -> typing.List[dict]:
        """ Get """

        if ids:
            if isinstance(ids, int):
                db_condition = {
                    'id': ids,
                }
            else:
                db_condition = {
                    'id': {'$in': ids},
                }
        else:
            db_condition = {}

        db_filter = {
            '_id': False,
        }

        if fields:
            for value in fields:
                db_filter[value] = True

        els = db[cls.db].find(db_condition, db_filter)
        els = list(els.sort('id', -1))

        last = count + offset if count else None
        els = els[offset:last]

        return els

    def save(
            self,
            **kw,
        ) -> typing.List[int]:
            """ Save """

            return
