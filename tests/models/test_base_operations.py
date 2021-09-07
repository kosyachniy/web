import time

import pytest

from api.models import Base, Attribute
from api.errors import ErrorWrong


class ObjectModel(Base):
    _db = 'tests'

    meta = Attribute(types=str)
    delta = Attribute(types=str, default='')
    extra = Attribute(types=str, default=lambda instance: f'u{instance.delta}o')
    multi = Attribute(types=list, default=[])


def test_load():
    now = time.time()
    instance = ObjectModel(
        name='test_load',
        user=2,
        status=3,
        meta='onigiri',
        delta='hinkali',
        extra='ramen',
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
    assert recieved.meta == 'onigiri'
    assert recieved.delta == 'hinkali'
    assert recieved.extra == 'ramen'

def test_list():
    now = time.time()

    instance1 = ObjectModel(
        name='test_list',
        user=2,
        status=3,
        meta='onigiri',
        delta='hinkali',
        extra='ramen',
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
        assert recieved1.meta == 'onigiri'
        assert recieved1.delta == 'hinkali'
        assert recieved1.extra == 'ramen'

    with recieved[0] as recieved2:
        assert isinstance(recieved2, ObjectModel)
        assert recieved2.id == instance2.id
        assert recieved2.created < now + 1
        assert recieved2.updated < now + 1

def test_update():
    instance = ObjectModel(
        name='test_create',
        delta='hinkali',
    )
    instance.save()

    assert instance.name == 'test_create'
    assert instance.meta is None
    assert instance.delta == 'hinkali'

    instance_id = instance.id
    instance = ObjectModel.get(ids=instance_id)

    instance.name = 'test_update'
    instance.meta = 'onigiri'

    instance.save()

    assert instance_id == instance.id

    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_update'
    assert instance.meta == 'onigiri'
    assert instance.delta == 'hinkali'

def test_update_empty():
    instance = ObjectModel(
        name='test_create',
        meta='onigiri',
    )
    instance.save()

    assert instance.name == 'test_create'
    assert instance.meta == 'onigiri'

    instance_id = instance.id
    instance = ObjectModel.get(ids=instance_id)

    instance.name = None

    instance.save()

    assert instance_id == instance.id

    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_create'
    assert instance.meta == 'onigiri'

def test_update_resave():
    instance = ObjectModel(
        name='test_create',
        delta='hinkali'
    )
    instance.save()

    instance_id = instance.id

    instance.name = 'test_update'
    instance.meta = 'onigiri'
    instance.save()

    assert instance_id == instance.id

    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_update'
    assert instance.meta == 'onigiri'
    assert instance.delta == 'hinkali'

def test_rm():
    instance = ObjectModel()
    instance.save()

    instance.rm()

    with pytest.raises(ErrorWrong):
        ObjectModel.get(ids=instance.id)

def test_rm_nondb():
    instance = ObjectModel()

    with pytest.raises(ErrorWrong):
        instance.rm()

def test_rm_attr():
    instance = ObjectModel(
        meta='onigiri',
        delta='hinkali',
    )
    instance.save()

    instance = ObjectModel.get(ids=instance.id)

    del instance.meta
    instance.delta = 'hacapuri'

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert instance.meta is None
    assert instance.delta == 'hacapuri'

def test_rm_attr_resave():
    instance = ObjectModel(
        name='test_attr_resave',
        meta='onigiri',
        delta='hinkali',
    )
    instance.save()

    del instance.meta
    instance.delta = 'hacapuri'

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_attr_resave'
    assert instance.meta is None
    assert instance.delta == 'hacapuri'

def test_reload():
    instance = ObjectModel(
        delta='hinkali',
    )
    instance.save()

    recieved1 = ObjectModel.get(ids=instance.id)
    recieved2 = ObjectModel.get(ids=instance.id)

    assert recieved1._specified_fields is None
    assert recieved2._specified_fields is None

    recieved1.delta = 'hacapuri'
    recieved1.save()

    assert recieved1.delta == 'hacapuri'
    assert recieved2.delta == 'hinkali'

    recieved2.reload()

    assert recieved2._specified_fields is None
    assert recieved2.id == recieved1.id == instance.id
    assert recieved2.delta == 'hacapuri'

    recieved1.reload()

    assert recieved1._specified_fields is None
    assert recieved1.id == recieved1.id == instance.id
    assert recieved1.delta == 'hacapuri'

def test_resave():
    instance = ObjectModel(
        delta='hinkali',
    )

    instance.save()

    updated = instance.updated

    instance.save()

    assert instance.updated == updated
