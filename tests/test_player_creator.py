from pysms.creators import create_player, PlayerCreateConfig
from pysms.models import Player, PlayerPosition


def test_create_player():
    player = create_player(PlayerCreateConfig(), PlayerPosition.GOALKEEPER)
    assert type(player) == Player
    assert player.position == PlayerPosition.GOALKEEPER
