import pytest

from pysms.models.player import player_contribution, player_max_contribution, PlayerPosition, Player

DEFENDER = Player(name="DF", stopping=4, tackling=16, passing=10, shooting=8, stamina=60, aggression=30)
DEFENDING_MIDFIELDER = Player(name="DF", stopping=4, tackling=10, passing=16, shooting=8, stamina=60, aggression=30)
ATTACKING_MIDFIELDER = Player(name="AM", stopping=4, tackling=8, passing=16, shooting=10, stamina=60, aggression=30)
FORWARD = Player(name="FW", stopping=4, tackling=8,
                    passing=10, shooting=16, stamina=60, aggression=30)


@pytest.mark.parametrize("position,expected", [
    (PlayerPosition.GOALKEEPER, 5400),
    (PlayerPosition.DEFENDER, 7000),
    (PlayerPosition.DEFENDING_MIDFIELDER, 7800),
    (PlayerPosition.ATTACKING_MIDFIELDER, 8000),
    (PlayerPosition.FORWARD, 7400),
])
def test_player_contribution(position: PlayerPosition, expected: int) -> None:
    contrib = player_contribution(ATTACKING_MIDFIELDER, position)
    assert contrib == expected


@pytest.mark.parametrize("player,exp_position,exp_contribution", [
    (DEFENDER, PlayerPosition.DEFENDER, 8000),
    (DEFENDING_MIDFIELDER, PlayerPosition.DEFENDING_MIDFIELDER, 8000),
    (ATTACKING_MIDFIELDER, PlayerPosition.ATTACKING_MIDFIELDER, 8000),
    (FORWARD, PlayerPosition.FORWARD, 8000),
])
def test_player_max_contribution(player: Player, exp_position: PlayerPosition, exp_contribution: int) -> None:
    position, contrib = player_max_contribution(player)
    assert position == exp_position
    assert contrib == exp_contribution
