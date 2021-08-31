import pytest

from api.funcs import generate
from api.models.user import User
# from api.errors import ErrorWrong


def test_repeated_login():
    login = generate(20)

    user = User(login=login.title())
    user.save()

    assert user.id

    with pytest.raises(ValueError): # TODO: ErrorWrong
        User(login=login.upper())

def test_repeated_mail():
    mail = f'{generate(10)}@{generate(5)}.{generate(5)}'

    user = User(mail=mail.title())
    user.save()

    assert user.id

    with pytest.raises(ValueError): # TODO: ErrorWrong
        User(mail=mail.upper())

def test_none_fields():
    user = User(
        id=None,
        login=None,
        password=None,
        avatar=None,
        name=None,
        surname=None,
        phone=None,
        phone_verified=None,
        mail=None,
        mail_verified=None,
        social=None,
        description=None,
        language=None,
        actions=None,
        online=None,
        user=None,
        created=None,
        updated=None,
        status=None,
    )

    assert user
    assert not user.id
    assert user.login == 'id0'

    user.save()

    assert user.id
    assert user.login != 'id0'
