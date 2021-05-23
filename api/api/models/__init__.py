"""
Base model of DB object
"""

import typing

from ..funcs import next_id
from ..funcs.mongodb import db


class Base:
    """ Base model """

    id: int = 0

    def __init__(self, data: dict = {}, **kwargs) -> None:
        if not data:
            data = kwargs

        for key, value in data.items():
            setattr(self, key, value)

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
