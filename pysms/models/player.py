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
