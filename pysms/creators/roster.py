import typing
import uuid

from pysms.models import Roster, Team, Player
from .player import create_player
from .team import create_team

PLAYERS_COUNT = 25


def create_roster(team: typing.Optional[Team] = None) -> Roster:
    if not team:
        team = create_team()

    players: typing.List[Player] = []
    for _ in range(PLAYERS_COUNT):
        players.append(create_player())
    return Roster(id=uuid.uuid4(), team=team, players=players)
