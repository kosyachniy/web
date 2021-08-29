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

def test_update():
    sub1 = SubObject(
        taiga=1,
    )
    sub2 = SubObject(
        taiga=1,
    )
    sub3 = SubObject(
        taiga=3,
    )
    sub4 = SubObject(
        taiga=4,
        tundra=1,
    )
    sub5 = SubObject(
        taiga=5,
    )
    sub6 = SubObject(
        taiga=6,
        tundra=1,
    )
    instance = ObjectModel(
        multi=[
            sub1.json(default=False),
            sub2.json(default=False),
            sub3.json(default=False),
            sub4.json(default=False),
            sub5.json(default=False),
            sub6.json(default=False),
        ],
    )

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 6

    instance.multi[1]['taiga'] = 2
    del instance.multi[3]['tundra']
    instance.multi[4]['taiga'] = 5
    instance.multi[5]['tundra'] = 0

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 6
    assert instance.multi[0]['id'] == sub1.id
    assert instance.multi[0]['taiga'] == 1
    assert instance.multi[1]['id'] == sub2.id
    assert instance.multi[1]['taiga'] == 2
    assert instance.multi[2]['id'] == sub3.id
    assert instance.multi[2]['taiga'] == 3
    assert instance.multi[3]['id'] == sub4.id
    assert instance.multi[3]['taiga'] == 4
    assert 'tundra' not in instance.multi[3]
    assert instance.multi[4]['id'] == sub5.id
    assert instance.multi[4]['taiga'] == 5
    assert instance.multi[5]['id'] == sub6.id
    assert instance.multi[5]['taiga'] == 6
    assert instance.multi[5]['tundra'] == 0

def test_replace():
    sub1 = SubObject(
        taiga=1,
    )
    sub2 = SubObject(
        taiga=2,
    )
    sub3 = SubObject(
        taiga=3,
        tundra=-1,
    )
    sub4 = SubObject(
        taiga=4,
        tundra=0,
    )
    instance = ObjectModel(
        multi=[
            sub1.json(default=False),
            sub2.json(default=False),
            sub3.json(default=False),
            sub4.json(default=False),
        ],
    )

    instance.save()
    instance = ObjectModel.get(ids=instance.id, fields={})

    assert len(instance.multi) == 0

    sub2.taiga = -1
    instance.multi.append(sub2.json(default=False))
    instance.multi.append({'id': sub3.id, 'taiga': 0})

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 4
    assert instance.multi[0]['id'] == sub1.id
    assert instance.multi[0]['taiga'] == 1
    assert instance.multi[1]['id'] == sub2.id
    assert instance.multi[1]['taiga'] == -1
    assert instance.multi[2]['id'] == sub3.id
    assert instance.multi[2]['taiga'] == 0
    assert 'tundra' not in instance.multi[2]
    assert instance.multi[3]['id'] == sub4.id
    assert instance.multi[3]['taiga'] == 4
    assert 'tundra' not in instance.multi[3]
