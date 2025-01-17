from typing import List
from fastapi import APIRouter, HTTPException
from models.player import Player, PlayerUpdate
from db.database import db
from mysql.connector import Error
router = APIRouter()

@router.get("/players", response_model=List[Player])
async def get_players():
    try:
        players = db.get_all_records("Players")
        return players
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Получить игрока по Steam ID
@router.get("/players/{steam_id}", response_model=Player)
async def get_player(steam_id: str):
    player = db.find_record_by_single_field("Players", "steam_id", steam_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player[0]  # Возвращаем первую запись, так как результат — список

# Добавить нового игрока
@router.post("/players", response_model=Player)
async def create_player(player: Player):
    try:
        db.insert_record("Players", player.dict())
        return player
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Обновить данные игрока
@router.put("/players/{steam_id}", response_model=Player)
async def update_player(steam_id: str, player_update: PlayerUpdate):
    existing_player = db.find_record_by_single_field("Players", "steam_id", steam_id)
    if not existing_player:
        raise HTTPException(status_code=404, detail="Player not found")
    updates = player_update.dict(exclude_unset=True)
    try:
        db.update_record("Players", {"steam_id": steam_id}, updates)
        return {**existing_player[0], **updates}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Удалить игрока
@router.delete("/players/{steam_id}")
async def delete_player(steam_id: str):
    existing_player = db.find_record_by_single_field("Players", "steam_id", steam_id)
    if not existing_player:
        raise HTTPException(status_code=404, detail="Player not found")
    try:
        db.delete_record_by_id("Players", existing_player[0]["id"])
        return {"detail": "Player deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")