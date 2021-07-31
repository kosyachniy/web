import time

import pytest

from api.models import Base


class ObjectModel(Base):
    _db = 'tests'


def test_simple():
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
