import os
import typing

import pydantic

from .persistence import Provider
from pysms.models import Player, Roster
import pysms.persistence.models as models


class FilesystemProvider(Provider):
    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    def load_player(self, player_id: str) -> Player:
        return pydantic.parse_file_as(
            path=f"{self._base_dir}/players/{player_id}.json", type_=Player)

    def save_player(self, player: Player) -> bool:
        with open(f"{self._base_dir}/players/{player.id}.json", "wt") as fh:
            fh.write(player.json(indent=2))
        return True

    def load_roster(self, roster_id: str) -> Roster:
        data = pydantic.parse_file_as(
            path=f"{self._base_dir}/rosters/{roster_id}.json", type_=models.Roster)
        return models.roster.inflate_roster(data, self)

    def save_roster(self, roster: Roster) -> bool:
        for player in roster.players:
            self.save_player(player)

        record = models.roster.deflate_roster(roster)
        with open(f"{self._base_dir}/rosters/{record.id}.json", "wt") as fh:
            fh.write(record.json(indent=2))
        return True
