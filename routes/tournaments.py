from typing import List
from fastapi import APIRouter, HTTPException
from models.tournament import Tournament, TournamentUpdate
from db.database import db
from mysql.connector import Error
router = APIRouter()

# Получить список всех турниров
@router.get("/tournaments", response_model=List[Tournament])
async def get_tournaments():
    try:
        tournaments = db.get_all_records("Tournaments")
        return tournaments
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Получить турнир по ID
@router.get("/tournaments/{tournament_id}", response_model=Tournament)
async def get_tournament(tournament_id: int):
    tournament = db.find_record_by_single_field("Tournaments", "id", tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament[0]

# Добавить новый турнир
@router.post("/tournaments", response_model=Tournament)
async def create_tournament(tournament: Tournament):
    try:
        db.insert_record("Tournaments", tournament.model_dump())
        return tournament
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Обновить турнир
@router.put("/tournaments/{tournament_id}", response_model=Tournament)
async def update_tournament(tournament_id: int, tournament_update: TournamentUpdate):
    existing_tournament = db.find_record_by_single_field("Tournaments", "id", tournament_id)
    if not existing_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    updates = tournament_update.dict(exclude_unset=True)
    try:
        db.update_record("Tournaments", {"id": tournament_id}, updates)
        return {**existing_tournament[0], **updates}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Удалить турнир
@router.delete("/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: int):
    existing_tournament = db.find_record_by_single_field("Tournaments", "id", tournament_id)
    if not existing_tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    try:
        db.delete_record_by_id("Tournaments", tournament_id)
        return {"detail": "Tournament deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
