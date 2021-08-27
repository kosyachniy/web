from api.models import Base, Attribute
from tests.models.test_base_init import ObjectModel


class SubObject(Base):
    _db = None

    id = Attribute(types=str)
    taiga = Attribute(types=int)
    tundra = Attribute(types=int, default=0)


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

def test_save_sub_partially():
    sub1 = SubObject(
        taiga=1,
    )
    instance = ObjectModel(
        multi=[sub1.json(default=False)],
    )

    instance.save()
    recieved1 = ObjectModel.get(ids=instance.id, fields={'delta'})

    assert recieved1.multi == []


    sub2 = SubObject()
    recieved1.multi += [sub2.json(default=False)]

    recieved1.save()
    recieved2 = ObjectModel.get(ids=instance.id, fields={'multi'})

    assert recieved2.id == instance.id

    with SubObject(recieved2.multi[1]) as recieved:
        assert recieved.id == sub2.id
        assert recieved.taiga is None

    with SubObject(recieved2.multi[0]) as recieved:
        assert recieved.id == sub1.id
        assert recieved.taiga == 1

def test_pull():
    sub1 = SubObject(
        taiga=1,
    )
    sub2 = SubObject(
        taiga=2,
    )
    sub3 = SubObject(
        taiga=3,
    )
    instance = ObjectModel(
        multi=[
            sub1.json(default=False),
            sub2.json(default=False),
            sub3.json(default=False),
        ],
    )

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 3

    instance.multi[2]['taiga'] = 0
    del instance.multi[0]

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 2
    assert instance.multi[0]['id'] == sub2.id
    assert instance.multi[0]['taiga'] == sub2.taiga
    assert instance.multi[1]['id'] == sub3.id
