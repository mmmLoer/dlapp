from datetime import datetime
from pydantic import BaseModel, SkipValidation
from typing import Optional

class Match(BaseModel):
    event_id: int
    match_date: SkipValidation[datetime]
    class Config:
        arbitrary_types_allowed = True
    duration: int
    team1_id: int
    team2_id: int
    score_team1: int = 0
    score_team2: int = 0

class MatchUpdate(BaseModel):
    event_id: Optional[int]
    match_date: Optional[datetime] # type: ignore
    class Config:
        arbitrary_types_allowed = True
    duration: Optional[int]
    team1_id: Optional[int]
    team2_id: Optional[int]
    score_team1: Optional[int]
    score_team2: Optional[int]

class MatchResult(BaseModel):
    match_id: int
    winner_team_id: int
    loser_team_id: int
    score: str

class MatchResultUpdate(BaseModel):
    match_id: Optional[int]
    winner_team_id: Optional[int]
    loser_team_id: Optional[int]
    score: Optional[str]