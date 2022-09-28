import typing
import uuid

import pydantic

from pysms.models import Roster, Team, Player, PlayerPosition
from .player import create_player, PlayerCreateConfig
from .team import create_team


class RosterCreateConfig(pydantic.BaseSettings):
    GK_COUNT: int = 3
    DF_COUNT: int = 8
    DM_COUNT: int = 3
    MF_COUNT: int = 8
    AM_COUNT: int = 3
    FW_COUNT: int = 5
    players: PlayerCreateConfig

    class Config:
        env_prefix: str = "PYSMS_ROSTER_"


def create_roster(config: RosterCreateConfig, team: typing.Optional[Team] = None) -> Roster:
    roster_composition = {
        PlayerPosition.GOALKEEPER: config.GK_COUNT,
        PlayerPosition.DEFENDER: config.DF_COUNT,
        PlayerPosition.DEFENDING_MIDFIELDER: config.DM_COUNT,
        PlayerPosition.MIDFIELDER: config.MF_COUNT,
        PlayerPosition.ATTACKING_MIDFIELDER: config.AM_COUNT,
        PlayerPosition.FORWARD: config.FW_COUNT,
    }

    if not team:
        team = create_team()

    players: typing.List[Player] = []
    for position, count in roster_composition.items():
        for _ in range(count):
            players.append(create_player(config.players, position))
    return Roster(id=uuid.uuid4(), team=team, players=players)
