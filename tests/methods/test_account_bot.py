import pytest
from libdev.gen import generate, generate_id

from models.user import User, process_lower
from services.request import Request
from routes.account.bot import handler, Type


@pytest.mark.asyncio
async def test_repeated_login():
    login = generate(20)
    user_old = User(login=login)

    user_old.save()

    request = Request(None, None, generate(), 2, 0)
    data = {
        'user': generate_id(),
        'login': login.upper(),
    }

    res = await handler(Type(**data), request)

    assert res.get('id')
    assert res.get('new')

    user_new = User.get(ids=res['id'], fields={'login'})

    assert user_new.login != process_lower(login)
    assert user_new.id != user_old.id
