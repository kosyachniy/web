import pytest

from api.funcs.mongodb import db, DuplicateKeyError
from api.models import Base, Attribute
from api.errors import ErrorRepeat


class ObjectModel(Base):
    _db = 'tests'

    meta = Attribute(types=str)
    delta = Attribute(types=str, default='')
    extra = Attribute(types=str, default=lambda instance: f'u{instance.delta}o')
    multi = Attribute(types=list, default=[])


def test_concurrently_init():
    instance = ObjectModel(
        meta='onigiri',
    )
    instance.save()

    instance = ObjectModel(
        id=instance.id,
    )

    with pytest.raises(ErrorRepeat):
        instance.save()

    instance.reload()

    assert instance.meta == 'onigiri'

def test_concurrently_create():
    instance = ObjectModel(
        meta='onigiri',
    )
    instance.save()

    instance = ObjectModel(
        id=instance.id,
        meta='ramen',
    )

    # UGLY: The piece of code was taken out

    data = instance.json(default=False)

    with pytest.raises(DuplicateKeyError):
        db[instance._db].insert_one({'_id': instance.id, **data})

    instance.reload()

    assert instance.meta == 'onigiri'

def test_concurrently_update():
    instance = ObjectModel(
        meta='onigiri',
    )
    instance.save()

    instance1 = ObjectModel.get(ids=instance.id, fields={'meta'})
    instance2 = ObjectModel.get(ids=instance.id, fields={'meta'})

    # Allowed parallel changes
    instance1.delta = 'sodzu'
    instance2.extra = 'sake'

    instance1.save()
    instance2.save()

    # Conflicting parallel changes
    instance1.meta = 'hinkali'
    instance2.meta = 'hacapuri'

    instance1.save()

    with pytest.raises(ErrorRepeat):
        instance2.save()

    instance.reload()

    assert instance.meta == 'hinkali'
    assert instance.delta == 'sodzu'
    assert instance.extra == 'sake'
