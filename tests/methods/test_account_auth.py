import pytest
from libdev.gen import generate

from models.user import User, process_lower
from services.request import Request
from routes.account.auth import handler, Type


class SIO:
    async def emit(name, data, room):
        pass


@pytest.mark.asyncio
async def test_repeated_login():
    login = generate(20)
    user_old = User(login=login, password='asd123')

    user_old.save()
    assert user_old.id
    assert user_old.login == process_lower(login)

    request = Request(None, None, generate(), 2, 0, SIO())
    data = {
        'login': login.upper(),
        'password': 'asd123',
    }

    res = await handler(Type(**data), request)

    assert res.get('id')
    assert res.get('new') == False

    user_new = User.get(ids=res['id'], fields={'login'})

    assert user_new.login == process_lower(login)
    assert user_new.id == user_old.id
