from typing import List
from fastapi import APIRouter, HTTPException, status
from models.match import Match, MatchUpdate
from db.database import db
from deadlockApi.metods.matches import matches
from mysql.connector import Error
router = APIRouter()

# Получить список всех матчей
@router.get("/matches", response_model=List[Match])
async def get_matches():
    try:
        matches = db.get_all_records("Matches")
        return matches
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Получить матч по ID
@router.get("/matches/{match_id}", response_model=Match)
async def get_match(match_id: int):
    match = db.find_record_by_single_field("Matches", "id", match_id)
    if not match:
        return status.HTTP_404_NOT_FOUND
    return match[0]

# Добавить новый матч
@router.post("/matches/{match_id}")
async def create_match(match_id: int):
    try:
        match = db.find_record_by_single_field("Matches", "id", match_id)
        if not match:
            matchData = await matches(match_id)
            
            return status.HTTP_201_CREATED
        else:
            return status.HTTP_409_CONFLICT
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Удалить матч
@router.delete("/matches/{match_id}")
async def delete_match(match_id: int):
    existing_match = db.find_record_by_single_field("Matches", "id", match_id)
    if not existing_match:
        raise HTTPException(status_code=404, detail="Match not found")
    try:
        db.delete_record_by_id("Matches", match_id)
        return {"detail": "Match deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
