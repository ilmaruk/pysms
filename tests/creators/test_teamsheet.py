from datetime import datetime
import pytest
import typing
import uuid

from pysms.creators.teamsheet import extract_players
from pysms.models import Player, PlayerPosition
from pysms.models.player import PlayerSide


@pytest.mark.parametrize("mult,expected", [
    ((1, 3, 2, 1), ("DF", "MF")),
    ((1, 2, 3, 2), ("MF", "FW")),
    ((1, 1, 2, 3), ("FW", "MF")),
])
def test_extract_players(mult: typing.Tuple[int, int, int, int], expected: typing.Tuple[str, str]) -> None:
    players = [
        make_player("DF", 4, 14, 10, 5),
        make_player("MF", 4, 9, 15, 10),
        make_player("FW", 4, 9, 8, 17),
    ]
    count = 2
    subset, _ = extract_players(players, count, mult)
    assert len(subset) == 2
    assert subset[0].name == expected[0]
    assert subset[1].name == expected[1]


def make_player(name: str, stopping: int, tackling: int, passing: int, shooting: int) -> Player:
    return Player(
        id=uuid.uuid4(), name=name, stopping=stopping, tackling=tackling,
        passing=passing, shooting=shooting,
        nationality="xyz", dob=datetime.now(), position=PlayerPosition.GOALKEEPER,
        side=PlayerSide.ANY, stamina=60, aggression=30
    )