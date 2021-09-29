"""
System parameters model of DB object
"""

from . import Base, Attribute


class System(Base):
    """ System """

    _name = 'system'

    id = Attribute(types=str)
    data = Attribute()
