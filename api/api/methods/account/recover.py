"""
The password recover method of the account object of the API
"""

from consys.errors import ErrorWrong, ErrorAccess

from api.lib import generate_password, BaseType, validate, report
from api.models.user import User, process_lower, pre_process_phone


class Type(BaseType):
    login: str

@validate(Type)
async def handle(request, data):
    """ Recover password """

    # No access
    if request.user.status < 2:
        raise ErrorAccess('recover')

    # Get

    new = False
    login = process_lower(data.login)
    users = User.get(login=login, fields={})

    if users:
        user = users[0]
    else:
        new = True

    if new:
        mail = process_lower(data.login)
        users = User.get(mail=mail, fields={})

        if users:
            user = users[0]
            new = False

    if new:
        phone = pre_process_phone(data.login)
        users = User.get(phone=phone, fields={})

        if users:
            user = users[0]
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
