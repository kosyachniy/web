import typing

from api._func import next_id
from api._func.mongodb import db


class Base:
    """ Base model """

    id: int = 0

    def __init__(self, data: dict = {}, **kwargs) -> None:
        if not data:
            data = kwargs

        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def get(
        cls,
        ids: typing.Union[typing.List[int], int, None] = None,
        *,
        fields: typing.Optional[typing.List[str]] = None,
        count: typing.Optional[int] = None,
        offset: int = 0,
        **kw,
    ) -> typing.List[dict]:
        return list(db[cls.db].find({'id': ids}))
