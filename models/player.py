from pydantic import BaseModel
from typing import Optional

class Player(BaseModel):
    steam_id: str
    nickname: str
    rank: Optional[int]
    role: Optional[str]

class PlayerUpdate(BaseModel):
    steam_id: Optional[str]
    nickname: Optional[str]
    rank: Optional[int]
    role: Optional[str]