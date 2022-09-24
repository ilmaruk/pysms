import typing

from pysms.models import Player, Roster


class Provider(typing.Protocol):
    def load_player(self, player_id: str) -> Player:
        pass

    def save_player(self, player: Player) -> bool:
        pass

    def load_roster(self, roster_id: str) -> Roster:
        pass

    def save_roster(self, roster: Roster) -> bool:
        pass
