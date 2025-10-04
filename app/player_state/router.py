from fastapi import APIRouter
from app.player_state.schema import PlayerStateUpdate
from app.player_state.models import PlayerState
from app.player_state.services import PlayerStateService

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
