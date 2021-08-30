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
