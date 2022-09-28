import pytest

from pysms.models.player import player_contribution, player_max_contribution, PlayerPosition, Player

MIDFIELDER = Player(name="MF", stopping=4, tackling=8,
                    passing=16, shooting=10, stamina=60, aggression=30)


@pytest.mark.parametrize("position,expected", [
    (PlayerPosition.GOALKEEPER, 4600),
    (PlayerPosition.DEFENDER, 7000),
    (PlayerPosition.MIDFIELDER, 8800),
    (PlayerPosition.FORWARD, 7400),
])
def test_player_contribution(position: PlayerPosition, expected: int) -> None:
    contrib = player_contribution(MIDFIELDER, position)
    assert contrib == expected


def test_player_max_contribution() -> None:
    position, contrib = player_max_contribution(MIDFIELDER)
    assert position == PlayerPosition.MIDFIELDER
    assert contrib == 8800
