import time

import pytest

from api.models import Base


class ObjectModel(Base):
    _db = 'tests'


def test_attr():
    now = time.time()
    instance = ObjectModel()

    assert instance.id == 0
    assert instance.name is None
    assert instance.user == 0
    assert instance.created < now + 1
    assert instance.updated is None
    assert instance.status is None

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

    with pytest.raises(AttributeError):
        assert instance['undefined_field']

def test_data():
    now = time.time()
    instance = ObjectModel({
        'id': 1,
        'name': 'test',
        'user': 2,
        'status': 3,
    })

    assert instance.id == 1
    assert instance.name == 'test'
    assert instance.created < now + 1
    assert instance.user == 2
    assert instance.status == 3

def test_kwargs():
    now = time.time()
    instance = ObjectModel(
        id=1,
        name='TEST',
        user=2,
        status=3,
    )

    assert instance.id == 1
    assert instance.name == 'TEST'
    assert instance.created < now + 1
    assert instance.user == 2
    assert instance.status == 3

def test_empty_save():
    instance = ObjectModel()

    now = time.time()
    instance.save()

    assert instance.id > 0
    assert instance.updated < now + 1

def test_save():
    instance = ObjectModel(
        name='test',
    )

    now = time.time()
    instance.save()

    assert instance.id > 0
    assert instance.updated < now + 1

def test_load():
    now = time.time()
    instance = ObjectModel(
        name='test_load',
        user=2,
        status=3,
    )
    instance.save()

    recieved = ObjectModel.get(ids=instance.id)

    assert isinstance(recieved, ObjectModel)
    assert recieved.id == instance.id
    assert recieved.name == 'test_load'
    assert instance.created < now + 1
    assert instance.updated < now + 1
    assert instance.user == 2
    assert instance.status == 3

def test_list():
    now = time.time()

    instance1 = ObjectModel(
        name='test_list',
        user=2,
        status=3,
    )
    instance1.save()

    instance2 = ObjectModel()
    instance2.save()

    recieved = ObjectModel.get(ids=(
        instance1.id,
        instance2.id,
    ))

    assert isinstance(recieved, list)

    with recieved[1] as recieved1:
        assert isinstance(recieved1, ObjectModel)
        assert recieved1.id == instance1.id
        assert recieved1.name == 'test_list'
        assert recieved1.created < now + 1
        assert recieved1.updated < now + 1
        assert recieved1.user == 2
        assert recieved1.status == 3

    with recieved[0] as recieved2:
        assert isinstance(recieved2, ObjectModel)
        assert recieved2.id == instance2.id
        assert recieved2.created < now + 1
        assert recieved2.updated < now + 1
