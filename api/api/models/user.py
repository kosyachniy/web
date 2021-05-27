"""
User model of DB object
"""

from . import Base


class User(Base):
    """ User """

    db = 'users'
