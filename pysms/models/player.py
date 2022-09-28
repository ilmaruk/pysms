import datetime
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
    id: uuid.UUID
    name: str
    nationality: str
    dob: datetime.date
    position: PlayerPosition
    side: PlayerSide
    stopping: int
    tackling: int
    passing: int
    shooting: int
    stamina: int
    aggression: int
    abilities: PlayerAbilities = PlayerAbilities()
    stats: PlayerStats = PlayerStats()
