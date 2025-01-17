from typing import List
from fastapi import APIRouter, HTTPException
from models.teamlist import TeamList, TeamListUpdate
from db.database import db
from mysql.connector import Error
router = APIRouter()

# Получить список всех списков команд
@router.get("/teamlists", response_model=List[TeamList])
async def get_teamlists():
    try:
        teamlists = db.get_all_records("TeamLists")
        return teamlists
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Получить список команд по ID
@router.get("/teamlists/{teamlist_id}", response_model=TeamList)
async def get_teamlist(teamlist_id: int):
    teamlist = db.find_record_by_single_field("TeamLists", "id", teamlist_id)
    if not teamlist:
        raise HTTPException(status_code=404, detail="Team list not found")
    return teamlist[0]

# Добавить новый список команд
@router.post("/teamlists", response_model=TeamList)
async def create_teamlist(teamlist: TeamList):
    try:
        db.insert_record("TeamLists", teamlist.dict())
        return teamlist
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Обновить данные списка команд
@router.put("/teamlists/{teamlist_id}", response_model=TeamList)
async def update_teamlist(teamlist_id: int, teamlist_update: TeamListUpdate):
    existing_teamlist = db.find_record_by_single_field("TeamLists", "id", teamlist_id)
    if not existing_teamlist:
        raise HTTPException(status_code=404, detail="Team list not found")
    
    updates = teamlist_update.dict(exclude_unset=True)
    try:
        db.update_record("TeamLists", {"id": teamlist_id}, updates)
        return {**existing_teamlist[0], **updates}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Удалить список команд
@router.delete("/teamlists/{teamlist_id}")
async def delete_teamlist(teamlist_id: int):
    existing_teamlist = db.find_record_by_single_field("TeamLists", "id", teamlist_id)
    if not existing_teamlist:
        raise HTTPException(status_code=404, detail="Team list not found")
    
    try:
        db.delete_record_by_id("TeamLists", teamlist_id)
        return {"detail": "Team list deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
