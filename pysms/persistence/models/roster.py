import typing
import uuid

import pydantic

from pysms import models
from ..persistence import Provider


class Roster(pydantic.BaseModel):
    id: uuid.UUID
    team: uuid.UUID
    players: typing.List[uuid.UUID]


def deflate_roster(src: models.Roster) -> Roster:
    return Roster(id=src.id, team=src.team.id, players=[player.id for player in src.players])


def inflate_roster(src: Roster, provider: Provider) -> models.Roster:
    team = models.Team(
        id=src.team,
        name="Genoa CFC 1893",
        short="gen"
    )
    players: typing.List[models.Player] = []
    for player_id in src.players:
        players.append(provider.load_player(player_id))
    return models.Roster(id=src.id, team=team, players=players)
