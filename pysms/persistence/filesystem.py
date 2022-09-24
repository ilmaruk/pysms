import os
import typing

import pydantic

from .persistence import Provider
from pysms.models import Player, Roster
import pysms.persistence.models as models

PLAYERS_DIR = "players"
ROSTERS_DIR = "rosters"
TEAMS_DIR = "teams"


class FilesystemProvider(Provider):
    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    def load_player(self, player_id: str) -> Player:
        path = os.path.join(self._base_dir, PLAYERS_DIR, f"{player_id}.json")
        return pydantic.parse_file_as(path=path, type_=Player)

    def save_player(self, player: Player) -> bool:
        path = os.path.join(self._base_dir, PLAYERS_DIR, f"{player.id}.json")
        with open(path, "wt") as fh:
            fh.write(player.json(indent=2))
        return True

    def load_roster(self, roster_id: str) -> Roster:
        path = os.path.join(self._base_dir, ROSTERS_DIR, f"{roster_id}.json")
        data = pydantic.parse_file_as(path=path, type_=models.Roster)
        return models.roster.inflate_roster(data, self)

    def save_roster(self, roster: Roster) -> bool:
        for player in roster.players:
            self.save_player(player)

        record = models.roster.deflate_roster(roster)
        path = os.path.join(self._base_dir, ROSTERS_DIR, f"{record.id}.json")
        with open(path, "wt") as fh:
            fh.write(record.json(indent=2))
        return True
