"""
Base model of DB object
"""

from abc import abstractmethod
from typing import Union, Optional, Any

from ..funcs import next_id
from ..funcs.mongodb import db


class Attribute:
    """ Descriptor """

    name: str = None
    types: Any = None
    default: Any = None

    def __init__(self, types, default=None):
        self.types = types
        self.default = default

    def __set_name__(self, instance, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value) -> None:
        if not isinstance(value, self.types):
            raise TypeError('type')

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

# pylint: disable=C0103,R0913
class Base:
    """ Base model """

    id = Attribute(int, 0)
    name = Attribute(str)
    created = Attribute(int)
    status = Attribute(int)

    @property
    @abstractmethod
    def db(self) -> str:
        """ Database name """

    def __init__(self, data: dict = None, **kwargs) -> None:
        if not data:
            data = kwargs

        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise AttributeError('key')

        super().__setattr__(name, value)

    @classmethod
    def get(
        cls,
        ids: Union[list[int], int, None] = None,
        fields: Union[list[str], tuple[str], set[str], None] = None,
        search: Optional[str] = None, # TODO
        count: Optional[int] = None,
        offset: int = 0,
    ) -> list[dict]:
        """ Get """

        process_one = False

        if ids:
            if isinstance(ids, int):
                process_one = True
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

        if process_one:
            return els[0]

        return els

    def save(
        self,
    ) -> list[int]:
        """ Save """

        # Edit
        if self.id:
            db[self.db].update_one(
                {'id': self.id},
                {'$set': self.__dict__},
            )

            return

        # Create
        self.id = next_id(self.db)
        db[self.db].insert_one(self.__dict__)
        del self.__dict__['_id']

        return
