import typing
import uuid

import pydantic

from .team import Team
from .player import Player


class Roster(pydantic.BaseModel):
    id: uuid.UUID
    team: Team
    players: typing.List[Player]
