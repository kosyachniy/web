"""
Payment model of User object
"""

from api.models import Base, Attribute


class Payment(Base):
    """ Payments data """

    _name = None

    id = Attribute(types=str)
    type = Attribute(types=str)
    card = Attribute(types=dict, default={})
    frequency = Attribute(types=int, default=30)
    value = Attribute(types=int)
    currency = Attribute(types=str)
    discount = Attribute(types=float)
