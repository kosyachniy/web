"""
The password recover method of the account object of the API
"""

from ...funcs import BaseType, validate, generate_password, report
from ...models.user import User, process_lower, pre_process_phone
from ...errors import ErrorWrong, ErrorAccess


class Type(BaseType):
    login: str

# pylint: disable=unused-argument
@validate(Type)
async def handle(this, request, data):
    """ Recover password """

    # No access
    if request.user.status < 2:
        raise ErrorAccess('recover')

    # Get

    new = False

    try:
        login = process_lower(data.login)
        user = User.get(login=login, fields={})[0]
    except:
        new = True

    if new:
        try:
            mail = process_lower(data.login)
            user = User.get(mail=mail, fields={})[0]
        except:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(data.login)
            user = User.get(phone=phone, fields={})[0]
        except:
            pass
        else:
            new = False

    if new:
        raise ErrorWrong('login')

    # Update password
    password = generate_password()
    user.password = password
    user.save()

    # Send
    # TODO: send by mail
    # TODO: send by SMS

    # Report
    await report.request(
        "Recover password",
        {'password': password, 'user': user.id},
    )
