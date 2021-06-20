"""
The editing method of the account object of the API
"""

from ...funcs import check_params, load_image
from ...funcs.mongodb import db
from ...errors import ErrorInvalid, ErrorUpload, ErrorAccess


async def handle(this, **x):
    """ Edit personal information """

    # Checking parameters
    check_params(x, (
        ('name', False, str),
        ('surname', False, str),
        ('login', False, str),
        ('description', False, str),
        ('mail', False, str),
        ('password', False, str),
        ('avatar', False, str),
        ('file', False, str),
        ('social', False, list, dict),
    ))

    # No access
    if this.user['status'] < 3:
        raise ErrorAccess('edit')

    # Name
    if 'name' in x:
        _check_name(x['name'])
        this.user['name'] = x['name'].title()

    # Surname
    if 'surname' in x:
        _check_surname(x['surname'])
        this.user['surname'] = x['surname'].title()

    # Login
    if 'login' in x:
        x['login'] = x['login'].lower()

        if this.user['login'] != x['login']:
            _check_login(x['login'], this.user)
            this.user['login'] = x['login']

    # Mail
    if 'mail' in x:
        _check_mail(x['mail'], this.user)

    # Password
    if 'password' in x and len(x['password']):
        this.user['password'] = _process_password(x['password'])

    # Change fields
    for i in ('description', 'mail', 'social'):
        if i in x:
            this.user[i] = x[i]

    # Avatar
    if 'avatar' in x:
        try:
            file_type = x['file'].split('.')[-1]

        # Invalid file extension
        except:
            raise ErrorInvalid('file')

        try:
            link = load_image(x['avatar'], file_type)
            this.user['avatar'] = link

        # Error loading photo
        except:
            raise ErrorUpload('avatar')

    # Save changes
    db.users.save(this.user)

    # Response

    res = dict()

    if 'avatar' in this.user:
        res['avatar'] = '/load/opt/' + this.user['avatar']
    else:
        res['avatar'] = 'user.png'

    return res
