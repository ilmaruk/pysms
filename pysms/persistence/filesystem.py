import pydantic

from .persistence import Provider
from pysms.models import Player


class FilesystemProvider(Provider):
    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    def load_player(self, player_id: str) -> Player:
        return pydantic.parse_file_as(
            path=f"{self._base_dir}/players/{player_id}.json", type_=Player)

    def save_player(self, player: Player) -> bool:
        with open(f"{self._base_dir}/players/{player.id}.json", "wt") as fh:
            fh.write(player.json())
