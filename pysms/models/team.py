import uuid

import pydantic


class Team(pydantic.BaseModel):
    id: uuid.UUID
    name: str
    short: str
