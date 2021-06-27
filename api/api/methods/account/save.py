"""
The editing method of the account object of the API
"""

from ...funcs import check_params
from ...models.user import User
from ...errors import ErrorAccess


async def handle(this, **x):
    """ Save personal information """

    # Checking parameters
    check_params(x, (
        ('login', False, str),
        ('password', False, str),
        ('avatar', False, str),
        ('name', False, str),
        ('surname', False, str),
        ('mail', False, str),
        ('description', False, str),
        ('language', False, (str, int)),
        ('social', False, list, dict),
    ))

    # No access
    if this.user['status'] < 3:
        raise ErrorAccess('edit')

    # Get
    user = User.get(ids=this.user.id)

    # Change fields
    user.login = x['login']
    user.password = x['password']
    user.avatar = x['avatar']
    user.name = x['name']
    user.surname = x['surname']
    user.mail = x['mail']
    user.description = x['description']
    user.language = x['language']
    user.social = x['social'] # TODO: checking

    # Save
    user.save()

    # Response
    return {
        'avatar': user.avatar \
            if (x['avatar'] and x['avatar'] != user.avatar) \
            else None,
    }
