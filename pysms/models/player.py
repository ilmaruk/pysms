import datetime
import uuid

import pydantic


class Player(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    nationality: str
    dob: datetime.date
