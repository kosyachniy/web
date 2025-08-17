from consys import make_base, Attribute

from lib import cfg


Base = make_base(
    host=cfg("mongo.host", "mongo"),
    name=cfg("PROJECT_NAME"),
    login=cfg("mongo.user"),
    password=cfg("mongo.pass"),
)


__all__ = (
    "Base",
    "Attribute",
)
