import pytest
from libdev.gen import generate

from api import Request
from api.models.user import User, process_lower
from api.methods.account.auth import handle


class This:
    class SIO:
        async def emit(name, data, room):
            pass

    sio = SIO()


@pytest.mark.asyncio
async def test_repeated_login():
    login = generate(20)
    user_old = User(login=login, password='asd123')

    user_old.save()
    assert user_old.id
    assert user_old.login == process_lower(login)

    request = Request(None, None, generate(), 2, 0)
    data = {
        'login': login.upper(),
        'password': 'asd123',
    }

    res = await handle(This(), request, data)

    assert res.get('id')
    assert res.get('new') == False

    user_new = User.get(ids=res['id'], fields={'login'})

    assert user_new.login == process_lower(login)
    assert user_new.id == user_old.id
