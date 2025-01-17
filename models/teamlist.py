from pydantic import BaseModel
from typing import List, Optional

# Модель для списков команд (TeamLists)
class TeamList(BaseModel):
    name: str
    description: Optional[str]
    teams_main: Optional[List[int]]  # JSON поле

class TeamListUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    teams_main: Optional[List[int]]