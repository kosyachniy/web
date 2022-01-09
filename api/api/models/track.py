"""
Action tracking model of DB object
"""

from api.models import Base, Attribute


class Track(Base):
    """ Track """

    _name = 'tracking'

    data = Attribute(types=dict)
    user = Attribute(default=0)
    context = Attribute(default=dict)
