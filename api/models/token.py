from models import Base, Attribute


class Token(Base):
    """Token"""

    _name = "tokens"

    id = Attribute(types=str)
    network = Attribute(types=int)
    ip = Attribute(types=str)
    utm = Attribute(types=str)
    user_agent = Attribute(types=str)
    extra = Attribute(types=dict)
