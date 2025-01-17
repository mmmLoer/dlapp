from datetime import datetime
from pydantic import BaseModel, SkipValidation
from typing import List, Optional

class Tournament(BaseModel):
    id: Optional[int]
    name: str
    description: str
    prize_pool: float
    start_date: datetime
    end_date: datetime
    location: str

    class Config:
        from_attributes = True  # Новый ключ

# Модель для обновления турнира (только для PUT запросов)
class TournamentUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    prize_pool: Optional[float]
    start_date: Optional[SkipValidation[datetime]] # type: ignore
    end_date: Optional[SkipValidation[datetime]] # type: ignore
    class Config:
        arbitrary_types_allowed = True
    location: Optional[str]

    class Config:
        from_attributes = True  # Новый ключ
