import typing
import uuid

from pysms.models import Roster, Team, Player
from .player import create_player

PLAYERS_COUNT = 25


def create_roster(team: typing.Optional[Team] = None) -> Roster:
    if not team:
        team = Team(id=uuid.uuid4(), name="Genoa CFC", short="gen")

    players: typing.List[Player] = []
    for _ in range(PLAYERS_COUNT):
        players.append(create_player())
    return Roster(id=uuid.uuid4(), team=team, players=players)
