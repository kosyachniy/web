"""
Job model of DB object
"""

from api.models import Base, Attribute


class Job(Base):
    """ Job """

    _name = 'jobs'

    method = Attribute(types=str)
    users = Attribute(types=list)
    data = Attribute()
