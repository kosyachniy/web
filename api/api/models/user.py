"""
User model of DB object
"""

from . import Base, Attribute


class User(Base):
    """ User """

    db = 'users'
    login = Attribute(str)
    password = Attribute(str)
    avatar = Attribute(str)
    surname = Attribute(str)
    mail = Attribute(str)
    social = Attribute(list, []) # TODO: list[dict]
    description = Attribute(str)
    language = Attribute(int, 0)
    funnel = Attribute(list, []) # TODO: list[dict]
    online = Attribute(list, []) # TODO: list[tuple]
    # TODO: phone
    # TODO: balance
    # TODO: rating
    # TODO: referal_parent
    # TODO: referal_code
