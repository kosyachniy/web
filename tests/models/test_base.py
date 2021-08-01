import time

import pytest

from api.errors import ErrorWrong
from api.models import Base, Attribute


class ObjectModel(Base):
    _db = 'tests'

    meta = Attribute(types=str)
    delta = Attribute(types=str, default='')
    extra = Attribute(types=str, default=lambda instance: f'u{instance.delta}o')
    multi = Attribute(types=list, default=[])

class SubObject(Base):
    _db = None

    id = Attribute(types=str)
    taiga = Attribute(types=int)
    tundra = Attribute(types=int, default=0)


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

def test_init_sub():
    sub = SubObject(
        taiga=0,
    )

    assert isinstance(sub.id, str)
    assert len(sub.id) == 32
    assert sub.taiga == 0
    assert sub.tundra == 0

def test_init_sub_with_id():
    sub = SubObject(
        id='1',
        tundra=1,
    )

    assert sub.id == '1'
    assert sub.taiga is None
    assert sub.tundra == 1

def test_init_with_sub():
    sub = SubObject(
        taiga=1,
    )
    instance = ObjectModel(
        multi=[sub.json(default=False)],
    )

    with SubObject(instance.multi[0]) as recieved:
        assert recieved.id == sub.id
        assert recieved.taiga == 1
        assert recieved.tundra == 0

def test_create_with_sub():
    sub = SubObject(
        taiga=1,
    )
    instance = ObjectModel(
        multi=[sub.json(default=False)],
    )

    instance.save()

    assert instance.id > 0

    instance = ObjectModel.get(ids=instance.id)

    with SubObject(instance.multi[0]) as recieved:
        assert recieved.id == sub.id
        assert recieved.taiga == 1
        assert recieved.tundra == 0
