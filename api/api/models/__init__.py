"""
Base model of DB object
"""

import time
from abc import abstractmethod
from typing import Union, Optional, Any, Callable
from copy import deepcopy

from ..funcs.mongodb import db
from ..errors import ErrorWrong


def _next_id(name):
    """ Next DB ID """

    id_last = list(db[name].find({}, {'id': True, '_id': False}).sort('id', -1))

    if id_last:
        return id_last[0]['id'] + 1

    return 1

def pre_process_created(cont):
    """ Creation time pre-processing """

    if isinstance(cont, int):
        return float(cont)

    return cont


class Attribute:
    """ Descriptor """

    name: str = None
    types: Any = None
    default: Any = None
    checking: Callable = None
    pre_processing: Callable = None
    processing: Callable = None

    def __init__(
        self,
        types,
        default=None,
        checking=None,
        pre_processing=None,
        processing=None,
    ):
        self.types = types
        self.default = default
        self.checking = checking
        self.pre_processing = pre_processing
        self.processing = processing

    def __set_name__(self, instance, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            if isinstance(self.default, Callable):
                return self.default(owner)

            return deepcopy(self.default)

        if self.name in instance.__dict__:
            return instance.__dict__[self.name]

        if self.default is not None:
            if isinstance(self.default, Callable):
                instance.__dict__[self.name] = self.default(instance)
            else:
                instance.__dict__[self.name] = deepcopy(self.default)

            return instance.__dict__[self.name]

        return None

    def __set__(self, instance, value) -> None:
        if self.pre_processing:
            value = self.pre_processing(value)

        if value is None:
            if self.name in instance.__dict__:
                del instance.__dict__[self.name]

            return

        if not isinstance(value, self.types):
            raise TypeError(self.name)

        if self.checking and not self.checking(instance.id, value):
            raise ValueError(self.name)

        if self.processing:
            value = self.processing(value)

        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

# pylint: disable=C0103,R0913
class Base:
    """ Base model """

    id = Attribute(types=int, default=0) # TODO: unique
    name = Attribute(types=str) # TODO: required
    user = Attribute(types=int, default=0)
    created = Attribute(types=float, pre_processing=pre_process_created)
    status = Attribute(types=int)
    # TODO: modified / updated

    @property
    @abstractmethod
    def _db(self) -> str:
        """ Database name """

    def __init__(self, data: dict = None, **kwargs) -> None:
        # Auto complete (instead of Attribute(auto=...))
        self.created = time.time()

        if not data:
            data = kwargs

        for name, value in data.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if not hasattr(self, name):
            raise AttributeError('key')

        super().__setattr__(name, value)

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def _is_default(self, name):
        """ Check the value for the default value """

        data = deepcopy(self)
        delattr(data, name)

        return getattr(self, name) == getattr(data, name)

    @classmethod
    def get(
        cls,
        ids: Union[list, tuple, set, int, str, None] = None,
        count: Optional[int] = None,
        offset: int = 0,
        search: Optional[str] = None, # TODO: name, cont, tags
        fields: Union[list[str], tuple[str], set[str], None] = None,
        **kwargs,
    ):
        """ Get instances of the object """

        process_one = False

        if ids:
            if isinstance(ids, (list, tuple, set)):
                db_condition = {
                    'id': {'$in': ids},
                }
            else:
                process_one = True
                db_condition = {
                    'id': ids,
                }
        else:
            db_condition = {}

        if kwargs:
            for arg in kwargs:
                db_condition[arg] = kwargs[arg]

        db_filter = {
            '_id': False,
        }

        if fields:
            db_filter['id'] = True

            for value in fields:
                db_filter[value] = True

        els = db[cls._db].find(db_condition, db_filter)

        # if 'search' in x and x['search']:
        #     x['search'] = x['search'].lower()
        #     i = 0

        #     while i < len(posts):
        #         cond_name = x['search'] not in posts[i]['name'].lower()
        #         # TODO: HTML tags
        #         cond_cont = x['search'] not in posts[i]['cont'].lower()
        #         cond_tags = all(
        #             x['search'] not in tag.lower()
        #             for tag in posts[i]['tags']
        #         ) if 'tags' in posts[i] else True

        #         if cond_name and cond_cont and cond_tags:
        #             del posts[i]
        #             continue

        #         i += 1

        #     for i in range(len(posts)):
        #         # del posts[i]['cont'] # !

        #         if 'tags' in posts[i]:
        #             del posts[i]['tags']

        if offset is None:
            offset = 0

        els = els.sort('id', -1)
        last = count + offset if count else None
        els = els[offset:last]
        els = list(map(cls, els))

        if process_one:
            if not els:
                raise ErrorWrong('ids')

            return els[0]

        if ids and len(ids) != len(els):
            raise ErrorWrong('ids')

        return els

    def save(
        self,
    ):
        """ Save the instance """

        # TODO: deleting values

        exists = db[self._db].count_documents({'id': self.id})

        # Edit
        if exists:
            db[self._db].update_one(
                {'id': self.id},
                {'$set': self.json(default=False)},
            )

            return

        # Create
        if self.id == 0: # NOTE: `id` may not be int
            self.id = _next_id(self._db)
        db[self._db].insert_one(self.json(default=False))

    def rm(
        self,
    ):
        """ Delete the instance """

        res = db[self._db].delete_one({'id': self.id}).deleted_count

        if not res:
            raise ErrorWrong('id')

    def json(
        self,
        default=True, # Return default values
        none=False, # Return None values
        fields=None,
    ):
        """ Get dictionary of the object

        If default is True and there are fields, it will return only fields with
        non-default values
        """

        data = {}

        for attr in dir(self):
            if fields and attr not in fields:
                continue

            value = getattr(self, attr)

            if attr[0] == '_' or callable(value):
                continue

            if not default and self._is_default(attr):
                continue

            if not none and value is None:
                continue

            data[attr] = value

        return data
