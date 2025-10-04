from fastapi import APIRouter, HTTPException
from player_state.models import PlayerState

router = APIRouter()

player_state = PlayerState()


@router.get("/player/state", response_model=PlayerState)
def get_player_state():
    return player_state


@router.post("/player/reset", response_model=PlayerState)
def reset_player_state():
    global player_state
    player_state = PlayerState()
    return player_state


@router.post("/player/update", response_model=PlayerState)
def update_player_state(updated_state: PlayerState):
    global player_state
    player_state = updated_state
    return player_state
