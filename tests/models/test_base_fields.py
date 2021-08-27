from api.models import Base, Attribute


class ObjectModel(Base):
    _db = 'tests'

    meta = Attribute(types=str)
    delta = Attribute(types=str, default='')
    extra = Attribute(types=str, default=lambda instance: f'u{instance.delta}o')
    multi = Attribute(types=list, default=[])


def test_get_with_fields():
    instance = ObjectModel(
        meta='onigiri',
        delta='hinkali',
    )

    instance.save()
    recieved = ObjectModel.get(ids=instance.id, fields={'delta'})

    assert recieved.id == instance.id
    assert recieved.meta is None
    assert recieved.delta == 'hinkali'
    assert recieved.extra == 'uhinkalio'
    assert recieved.created is None
    assert recieved.updated is None

def test_save_none_with_fields():
    instance = ObjectModel(
        meta='onigiri',
        delta='hinkali',
    )

    instance.save()
    recieved1 = ObjectModel.get(ids=instance.id, fields={'delta'})

    recieved1.extra = 'ramen'

    recieved1.save()
    recieved2 = ObjectModel.get(ids=instance.id)

    assert recieved2.id == instance.id
    assert recieved2.meta == 'onigiri'
    assert recieved2.delta == 'hinkali'
    assert recieved2.extra == 'ramen'
    assert recieved2.created == instance.created
    assert recieved2.updated != instance.updated

def test_save_data_with_fields():
    instance = ObjectModel(
        name='test_save_fields',
        meta='onigiri',
        delta='hinkali',
    )

    instance.save()
    recieved1 = ObjectModel.get(ids=instance.id, fields={'name', 'delta'})

    recieved1.name = None
    recieved1.delta = 'hacapuri'

    recieved1.save()
    recieved2 = ObjectModel.get(ids=instance.id)

    assert recieved2.id == instance.id
    assert recieved2.name == 'test_save_fields'
    assert recieved2.meta == 'onigiri'
    assert recieved2.delta == 'hacapuri'
    assert recieved2.extra == 'uhacapurio'
    assert recieved2.created == instance.created
    assert recieved2.updated != instance.updated

def test_reload_with_fields():
    # now = time.time()

    instance = ObjectModel(
        name='test_reload_fields',
        meta='onigiri',
        delta='hinkali',
        multi=[1, 2, 3],
    )
    instance.save()

    recieved = ObjectModel.get(ids=instance.id, fields={'meta'})

    assert set(recieved._loaded_values) == {'id', 'meta'}
    assert recieved._specified_fields == {'id', 'meta'}

    recieved.delta = 'hacapuri'
    recieved.multi = [4, 5, 6]
    recieved.save()

    recieved.reload(fields={'meta', 'extra', 'multi'})

    assert set(recieved._loaded_values) == {
        'id', # Default
        'meta', # Specified
        'multi', # Specified
        # 'delta', # Changed
        # 'updated', # Auto changed
    }
    assert recieved._specified_fields == {
        'id',
        'meta',
        'extra',
        'multi',
    }
    assert recieved.id == instance.id
    assert recieved.name is None
    assert recieved.meta == 'onigiri'
    assert recieved.delta == '' # default
    assert recieved.extra == 'uo' # default
    assert recieved.multi == [4, 5, 6] # new
    assert recieved.created is None
    assert recieved.updated is None
