"""
Payment model of User object
"""

from models import Base, Attribute


class Payment(Base):
    """ Payments data """

    _name = None

    id = Attribute(types=str)
    type = Attribute(types=str)
    card = Attribute(types=dict)
    frequency = Attribute(types=int, default=30) # Days
    value = Attribute(types=int)
    currency = Attribute(types=str)
    discount = Attribute(types=float)
