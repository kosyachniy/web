import pytest
from libdev.gen import generate
from consys.errors import ErrorInvalid

from models.user import User


def test_repeated_login():
    login = generate(20)

    user = User(login=login.title())
    user.save()

    assert user.id

    with pytest.raises(ErrorInvalid):
        User(login=login.upper())

def test_repeated_mail():
    mail = f'{generate(10)}@{generate(5)}.{generate(5)}'

    user = User(mail=mail.title())
    user.save()

    assert user.id

    with pytest.raises(ErrorInvalid):
        User(mail=mail.upper())

def test_none_fields():
    user = User(
        id=None,
        login=None,
        password=None,
        image=None,
        name=None,
        surname=None,
        title=None,
        birth=None,
        sex=None,
        phone=None,
        phone_verified=None,
        mail=None,
        mail_verified=None,
        social=None,
        description=None,
        locale=None,
        status=None,
        rating=None,
        discount=None,
        balance=None,
        subscription=None,
        utm=None,
        pay=None,
        mailing=None,
        last_online=None,
        user=None,
        created=None,
        updated=None,
    )

    assert user
    assert not user.id
    assert user.login == 'id0'

    user.save()

    assert user.id
    assert user.login != 'id0'

def test_phone_processing():
    assert User(phone='+7 (969) 736-67-30').phone == 79697366730
    assert User(phone='79697366730').phone == 79697366730
    assert User(phone=89697366730).phone == 79697366730
    assert User(phone='8 9697366730').phone == 79697366730

    with pytest.raises(ErrorInvalid):
        User(phone='(969) 7366730')

    with pytest.raises(ErrorInvalid):
        User(phone='abcdefghijklmn')

    with pytest.raises(ErrorInvalid):
        User(phone='')
