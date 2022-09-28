import typing
import uuid

from pysms.models import Roster, Team, Player, PlayerPosition
from .player import create_player
from .team import create_team

ROSTER_COMPOSITION = {
    PlayerPosition.GOALKEEPER: 3,
    PlayerPosition.DEFENDER: 8,
    PlayerPosition.DEFENDING_MIDFIELDER: 3,
    PlayerPosition.MIDFIELDER: 8,
    PlayerPosition.ATTACKING_MIDFIELDER: 3,
    PlayerPosition.FORWARD: 5,
}


def create_roster(team: typing.Optional[Team] = None) -> Roster:
    if not team:
        team = create_team()

    players: typing.List[Player] = []
    for position, count in ROSTER_COMPOSITION.items():
        for _ in range(count):
            players.append(create_player(position))
    return Roster(id=uuid.uuid4(), team=team, players=players)
