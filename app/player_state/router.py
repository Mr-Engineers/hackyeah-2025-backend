from fastapi import APIRouter, HTTPException
from app.player_state.models import PlayerState
import redis
import json

router = APIRouter()

player_state = PlayerState()

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

REDIS_KEY = "player_state"

def save_state(state: PlayerState):
    """Zapisuje stan gracza do Redis"""
    r.set(REDIS_KEY, state.json())


def load_state() -> PlayerState:
    """Ładuje stan gracza z Redis"""
    data = r.get(REDIS_KEY)
    if data:
        return PlayerState.parse_raw(data)
    default_state = PlayerState()
    save_state(default_state)
    return default_state


@router.get("/player/state", response_model=PlayerState)
def get_player_state():
    """Zwraca aktualny stan gracza"""
    return load_state()


@router.post("/player/reset", response_model=PlayerState)
def reset_player_state():
    """Resetuje stan gracza do wartości domyślnych"""
    new_state = PlayerState()
    save_state(new_state)
    return new_state


@router.post("/player/update", response_model=PlayerState)
def update_player_state(updated_state: PlayerState):
    """Aktualizuje stan gracza na podstawie danych wejściowych"""
    save_state(updated_state)
    return updated_state