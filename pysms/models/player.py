import datetime
import typing
import uuid
from enum import Enum

import pydantic


class PlayerPosition(str, Enum):
    GOALKEEPER = "GK"
    DEFENDER = "DF"
    DEFENDING_MIDFIELDER = "DM"
    MIDFIELDER = "MF"
    ATTACKING_MIDFIELDER = "AM"
    FORWARD = "FW"


class PlayerSide(str, Enum):
    ANY = "RLC"
    RIGHT_LEFT = "RL"
    RIGHT_CENTRE = "RC"
    LEFT_CENTRE = "LC"
    RIGHT = "R"
    LEFT = "L"
    CENTRE = "C"


class PlayerAbilities(pydantic.BaseModel):
    stopping: int = 300
    tackling: int = 300
    passing: int = 300
    shooting: int = 300


class PlayerStats(pydantic.BaseModel):
    games: int = 0
    saves: int = 0
    tackles: int = 0
    keypasses: int = 0
    shots: int = 0
    goals: int = 0
    assists: int = 0
    dp: int = 0
    injury: int = 0
    suspension: int = 0
    fitness: int = 100


class Player(pydantic.BaseModel):
    id: typing.Optional[uuid.UUID]
    name: str
    nationality: typing.Optional[str]
    dob: typing.Optional[datetime.date]
    position: typing.Optional[PlayerPosition]
    side: typing.Optional[PlayerSide]
    stopping: int
    tackling: int
    passing: int
    shooting: int
    stamina: int
    aggression: int
    abilities: PlayerAbilities = PlayerAbilities()
    stats: PlayerStats = PlayerStats()

    # TODO: remove
    def __str__(self):
        return f"{self.name},{self.position},{self.stopping},{self.tackling},{self.passing},{self.shooting}"

    # TODO: remove
    def __repr__(self):
        return f"{self.name},{self.position},{self.stopping},{self.tackling},{self.passing},{self.shooting}"

CONTRIBUTION_WEIGHT_HIGH = 3
CONTRIBUTION_WEIGHT_MEDIUM = 2
CONTRIBUTION_WEIGHT_LOW = 1
CONTRIBUTION_WEIGHTS = {
    PlayerPosition.GOALKEEPER: (CONTRIBUTION_WEIGHT_HIGH, CONTRIBUTION_WEIGHT_MEDIUM, CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_LOW),
    PlayerPosition.DEFENDER: (CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_HIGH, CONTRIBUTION_WEIGHT_MEDIUM, CONTRIBUTION_WEIGHT_LOW),
    PlayerPosition.DEFENDING_MIDFIELDER: (CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_MEDIUM, CONTRIBUTION_WEIGHT_HIGH, CONTRIBUTION_WEIGHT_LOW),
    PlayerPosition.ATTACKING_MIDFIELDER: (CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_HIGH, CONTRIBUTION_WEIGHT_MEDIUM),
    PlayerPosition.FORWARD: (CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_MEDIUM, CONTRIBUTION_WEIGHT_HIGH),
}


def player_contribution(player: Player, position: PlayerPosition) -> int:
    """Calculate the contribution of a player in a specific position.
    """
    st_w, tk_w, ps_w, sh_w = CONTRIBUTION_WEIGHTS.get(
        position, (CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_LOW, CONTRIBUTION_WEIGHT_LOW))
    return (player.stopping * st_w + player.tackling * tk_w + player.passing * ps_w + player.shooting * sh_w) * player.stats.fitness


def player_max_contribution(player: Player) -> typing.Tuple[PlayerPosition, int]:
    """Determine which position a player gives their max contribution in.
    """
    max_position: PlayerPosition
    max_contribution = -1
    for position in CONTRIBUTION_WEIGHTS.keys():
        contrib = player_contribution(player, position)
        if max_contribution < contrib:
            max_contribution = contrib
            max_position = position
    return max_position, max_contribution
