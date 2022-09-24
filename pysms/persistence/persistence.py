import typing

from pysms.models import Player


class Provider(typing.Protocol):
    def load_player(self, player_id: str) -> Player:
        pass

    def save_player(self, player: Player) -> bool:
        pass
