from typing import List
from fastapi import APIRouter, HTTPException
from models.team import Team, TeamUpdate
from db.database import db
from mysql.connector import Error
router = APIRouter()

# Получить список всех команд
@router.get("/teams", response_model=List[Team])
async def get_teams():
    try:
        teams = db.get_all_records("Teams")
        return teams
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Получить команду по ID
@router.get("/teams/{team_id}", response_model=Team)
async def get_team(team_id: int):
    team = db.find_record_by_single_field("Teams", "id", team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team[0]

# Добавить новую команду
@router.post("/teams", response_model=Team)
async def create_team(team: Team):
    try:
        db.insert_record("Teams", team.dict())
        return team
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Обновить данные команды
@router.put("/teams/{team_id}", response_model=Team)
async def update_team(team_id: int, team_update: TeamUpdate):
    existing_team = db.find_record_by_single_field("Teams", "id", team_id)
    if not existing_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    updates = team_update.dict(exclude_unset=True)
    try:
        db.update_record("Teams", {"id": team_id}, updates)
        return {**existing_team[0], **updates}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Удалить команду
@router.delete("/teams/{team_id}")
async def delete_team(team_id: int):
    existing_team = db.find_record_by_single_field("Teams", "id", team_id)
    if not existing_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    try:
        db.delete_record_by_id("Teams", team_id)
        return {"detail": "Team deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
