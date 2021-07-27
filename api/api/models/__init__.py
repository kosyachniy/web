"""
Base model of DB object
"""

import time
from abc import abstractmethod
from typing import Union, Optional, Any, Callable
from copy import deepcopy

from ..funcs import generate
from ..funcs.mongodb import db
from ..errors import ErrorWrong, ErrorUnsaved


def _next_id(name):
    """ Next DB ID """

    id_last = list(db[name].find({}, {'id': True, '_id': False}).sort('id', -1))

    if id_last:
        return id_last[0]['id'] + 1

    return 1

def _search(value, search):
    """ Search for matches by value """

    if isinstance(value, str):
        return search in value.lower()

    if isinstance(value, (int, float)):
        return search.isdigit() and int(search) == value

    if isinstance(value, (list, tuple, set)):
        for el in value:
            if _search(el, search):
                return True
        return False

    if isinstance(value, dict):
        for el in value.values():
            if _search(el, search):
                return True
        return False

    return False

def _is_subobject(data):
    """ Checking for subobject

    Theoretically, this is object, which has own model, but without DB
    Practically, this is dictionary with id
    """

    if (
        isinstance(data, (list, tuple, set))
        and data and isinstance(data[0], dict)
        and 'id' in data[0]
    ):
        return True

    return False

def pre_process_time(cont):
    """ Time pre-processing """

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
        if value is None:
            return

        if self.pre_processing:
            value = self.pre_processing(value)

        # if value is None:
        #     if self.name in instance.__dict__:
        #         del instance.__dict__[self.name]

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

class Base:
    """ Base model """

    id = Attribute(types=int, default=0) # TODO: unique
    name = Attribute(types=str) # TODO: required
    user = Attribute(types=int, default=0)
    created = Attribute(types=float, pre_processing=pre_process_time)
    updated = Attribute(types=float, pre_processing=pre_process_time)
    status = Attribute(types=int)
    # TODO: modified / updated

    @property
    @abstractmethod
    def _db(self) -> str:
        """ Database name """

        return None

    _search_fields = ['name']

    def __init__(self, data: dict = None, **kwargs) -> None:
        # Auto complete (instead of Attribute(auto=...))
        self.created = time.time()

        if not data:
            data = kwargs

        # Subobject
        if data.get('id', None) is None and self._db is None:
            data['id'] = generate()

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

    def __repr__(self):
        return f'{self.__class__.__name__}({self.json(none=True)})'

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
        search: Optional[str] = None,
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
            for key, value in kwargs.items():
                db_condition[key] = value

        db_filter = {
            '_id': False,
        }

        if fields:
            db_filter['id'] = True

            for value in fields:
                db_filter[value] = True

        res = db[cls._db].find(db_condition, db_filter)
        els = []

        if search:
            search = search.lower()

            for el in res:
                match = False

                for field in cls._search_fields:
                    if field in el:
                        if _search(el[field], search):
                            match = True
                            break

                if match:
                    els.append(el)

            els.sort(key=lambda el: el['id'], reverse=True)

        else:
            els = res.sort('id', -1)

        if offset is None:
            offset = 0

        last = count + offset if count else None
        els = els[offset:last]
        els = list(map(cls, els))

        if process_one:
            if not els:
                raise ErrorWrong('id')

            return els[0]

        if ids and len(ids) != len(els):
            raise ErrorWrong('id')

        return els

    def save(
        self,
    ):
        """ Save the instance

        Default and None values are not written to DB
        To delete attributes, use .rm_attr()

        If the object has subobjects (list of dicts with id),
        1. there will be added only subobjects with new ids,
        2. unspecified subobjects won't be deleted,
        3. the order of subobjects won't be changed.
        To delete subobjects, use .rm_sub()
        """

        # TODO: changed?

        exists = db[self._db].count_documents({'id': self.id})

        # Update time
        self.updated = time.time()

        # Edit
        if exists:
            data = self.json(default=False)

            # Adding subobjects to existing ones

            data_set = {}
            data_push = {}

            for key, value in data.items():
                if _is_subobject(value):
                    data_push[key] = value
                    continue

                data_set[key] = value

            if data_push:
                fields = {'_id': False, **{field: True for field in data_push}}
                data_prepush = db[self._db].find_one({'id': self.id}, fields)

                # TODO: remake to MongoDB request selection
                for field in data_prepush:
                    for value in data_prepush[field]:
                        i = 0

                        while i < len(data_push[field]):
                            if data_push[field][i]['id'] == value['id']:
                                del data_push[field][i]
                                break

                            i += 1

            # Update

            db_request = {'$set': data_set}

            if data_push:
                db_request['$push'] = {
                    key: {'$each': value}
                    for key, value in data_push.items()
                }

            db[self._db].update_one({'id': self.id}, db_request)

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

    def rm_attr(
        self,
        fields: Union[list[str], tuple[str], set[str], str, None],
    ):
        """ Delete the attribute of the instance

        After calling this function, all unsaved instance data will be erased
        """

        if not db[self._db].count_documents({'id': self.id}):
            raise ErrorUnsaved('id')

        # Update time
        self.updated = time.time()

        if isinstance(fields, str):
            fields = {fields}

        db[self._db].update_one(
            {'id': self.id},
            {
                '$set': {'updated': self.updated},
                '$unset': {field: '' for field in fields},
            }
        )

        self.reload()

    def rm_sub(
        self,
        field: str,
        ids: Union[int, str],
    ):
        """ Delete the subobject of the instance

        After calling this function, all unsaved instance data will be erased
        """

        if not db[self._db].count_documents({'id': self.id}):
            raise ErrorUnsaved('id')

        # Update time
        self.updated = time.time()

        db[self._db].update_one(
            {'id': self.id},
            {
                '$set': {'updated': self.updated},
                '$pull': {field: {'id': ids}},
            }
        )

        self.reload()

        if self._is_default(field):
            db[self._db].update_one(
                {'id': self.id},
                {'$unset': {field: ''}}
            )

    def json(
        self,
        default=True, # Return default values
        none=False, # Return None values
        fields=None,
    ):
        """ Get dictionary of the object

        If default is True and there are fields,
        it will return only fields with non-default values
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

    def reload(
        self,
    ):
        """ Update the object according to the data from the DB

        After calling this function, all unsaved instance data will be erased
        """

        try:
            data = self.get(ids=self.id, fields=self.__dict__)
        except ErrorWrong as e:
            raise ErrorUnsaved(e)

        self.__dict__ = data.json(default=False)
