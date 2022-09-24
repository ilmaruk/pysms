from pysms.creators import create_player
from pysms.models import Player


def test_create_player():
    player = create_player()
    print(player.json())
    assert type(player) == Player
