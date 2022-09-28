import typing

import pydantic

from . import Team, Player

Formation = typing.Tuple[int, int, int]
ALLOWED_FORMATIONS: typing.List[Formation] = [
    (6, 3, 1),
    (5, 4, 1),
    (5, 3, 2),
    (4, 4, 2),
    (4, 3, 3),
    (3, 6, 1),
    (3, 5, 2),
    (3, 4, 3),
]


class Teamsheet(pydantic.BaseModel):
    team: Team
    formation: typing.Optional[Formation]
    field: typing.List[Player]
    bench: typing.List[Player]
