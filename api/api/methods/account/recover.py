"""
The password recover method of the account object of the API
"""

from ...funcs import check_params, generate_password, report
from ...models.user import User, process_login, process_lower, pre_process_phone
from ...errors import ErrorWrong


# pylint: disable=unused-argument
async def handle(this, **x):
    """ Recover password """

    # Checking parameters
    check_params(x, (
        ('login', True, str),
    ))

    # Get

    new = False

    try:
        login = process_login(x['login'])
        user = User.get(login=login, fields={})[0]
    except:
        new = True

    if new:
        try:
            mail = process_lower(x['login'])
            user = User.get(mail=mail, fields={})[0]
        except:
            pass
        else:
            new = False

    if new:
        try:
            phone = pre_process_phone(x['login'])
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
    report(f"Recover password `{password }` for user={user.id}", 1)
    # TODO: warning -> request
