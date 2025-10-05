from fastapi import APIRouter, Depends, HTTPException
from app.player_state.schema import PlayerStateUpdate
from app.player_state.models import PlayerState
from app.player_state.services import PlayerStateService
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()
service = PlayerStateService()

@router.get("/player/state", response_model=PlayerState)
def get_player_state():
    return service.load_state()

@router.post("/player/reset", response_model=PlayerState)
def reset_player_state():
    return service.reset_state()

@router.post("/player/update", response_model=PlayerState)
def update_player_state(updated: PlayerStateUpdate):
    current_state = service.load_state()
    updated_data = updated.dict(exclude_unset=True)
    new_state = current_state.copy(update=updated_data)
    return service.update_state(new_state)


@router.post("/player/pension", response_model=float)
def calculate_pension_endpoint():

    state = service.load_state()

    if not state:
        raise HTTPException(status_code=404, detail="Stan gracza nie został znaleziony")

    expected_lifetime_months = 264,2
    if state.sex=="Mężczyzna":
        expected_lifetime_months = 218.9
    pension = state.calculate_pension(expected_lifetime_months)
    return pension