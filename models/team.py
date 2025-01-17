from pydantic import BaseModel
from typing import Optional

class Team(BaseModel):
    name: str
    logo: Optional[str]
    description: Optional[str]

class TeamUpdate(BaseModel):
    name: Optional[str]
    logo: Optional[str]
    description: Optional[str]