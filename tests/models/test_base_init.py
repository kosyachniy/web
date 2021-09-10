import time
import json

import pytest

from api.models import Base, Attribute


class ObjectModel(Base):
    _db = 'tests'

    meta = Attribute(types=str)
    delta = Attribute(types=str, default='')
    extra = Attribute(types=str, default=lambda instance: f'u{instance.delta}o')
    teta = Attribute(types=str, ignore=True)
    multi = Attribute(types=list, default=[])


def test_attr():
    now = time.time()
    instance = ObjectModel()

    assert instance.id == 0
    assert instance.name is None
    assert instance.user == 0
    assert instance.created < now + 1
    assert instance.updated is None
    assert instance.status is None
    assert instance.meta is None
    assert instance.delta == ''
    assert instance.extra == 'uo'

    with pytest.raises(AttributeError):
        assert instance.undefined_field

def test_item():
    now = time.time()
    instance = ObjectModel()

    assert instance['id'] == 0
    assert instance['name'] is None
    assert instance['user'] == 0
    assert instance['created'] < now + 1
    assert instance['updated'] is None
    assert instance['status'] is None
    assert instance['meta'] is None
    assert instance['delta'] == ''
    assert instance['extra'] == 'uo'

    with pytest.raises(AttributeError):
        assert instance['undefined_field']

def test_data():
    now = time.time()
    instance = ObjectModel({
        'id': 1,
        'name': 'test_data',
        'user': 2,
        'status': 3,
        'meta': 'onigiri',
        'delta': 'hinkali',
        'extra': 'ramen',
    })

    assert instance.id == 1
    assert instance.name == 'test_data'
    assert instance.created < now + 1
    assert instance.user == 2
    assert instance.status == 3
    assert instance.meta == 'onigiri'
    assert instance.delta == 'hinkali'
    assert instance.extra == 'ramen'

def test_kwargs():
    now = time.time()
    instance = ObjectModel(
        id=1,
        name='test_kwargs',
        user=2,
        status=3,
        meta='oNiGiRi',
        delta='HINKali',
        extra='RAMEN',
    )

    assert instance.id == 1
    assert instance.name == 'test_kwargs'
    assert instance.created < now + 1
    assert instance.user == 2
    assert instance.status == 3
    assert instance.meta == 'oNiGiRi'
    assert instance.delta == 'HINKali'
    assert instance.extra == 'RAMEN'

def test_create_empty():
    instance = ObjectModel()

    now = time.time()
    instance.save()

    assert instance.id > 0
    assert instance.updated < now + 1

def test_create():
    instance = ObjectModel(
        name='test_create',
        meta='onigiri',
    )

    now = time.time()
    instance.save()

    assert instance.id > 0
    assert instance.updated < now + 1

def test_init_print():
    instance = ObjectModel(
        meta='onigiri',
        multi=[1, 2, 3],
    )

    text = str(instance)
    assert text[:19] == 'Object ObjectModel('
    assert text[-1] == ')'
    assert json.loads(text[19:-1]) == {
        'id': 0,
        'name': None,
        'meta': 'onigiri',
        'delta': '',
        'extra': 'uo',
        'teta': None,
        'multi': [1, 2, 3],
        'status': None,
        'user': 0,
        'created': instance.created,
        'updated': None,
    }

def test_ignore():
    # Initialization error
    with pytest.raises(TypeError):
        ObjectModel(meta=1)

    # Ignore in case of an error during initialization
    instance = ObjectModel(teta=1)
    assert instance.teta is None

    # Ignore in case of an error during assignment
    instance.teta = 1
    assert instance.teta is None

    # Ignore in case of an error during initialization
    instance = ObjectModel(ignore={'meta'}, meta=1)
    assert instance.meta is None

    # Ignore in case of an error during assignment
    with pytest.raises(TypeError):
        instance.meta = 1
