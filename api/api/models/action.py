"""
Action model of User object
"""

from . import Base, Attribute


class Action(Base):
    """ Action """

    id = Attribute(types=str)
    details = Attribute(types=dict, default={})
