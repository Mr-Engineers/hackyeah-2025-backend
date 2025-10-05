from fastapi import APIRouter

from app.events.models import BadEvent
from app.player_state.services import PlayerStateService

from ..events.bad_events_manager import draw_random_bad_event
from app.player_state.router import get_player_state, update_player_state

router = APIRouter()
service = PlayerStateService()

@router.get("/badevent", response_model=BadEvent)
def get_bad_event():
    player_state = get_player_state()
    random_event = draw_random_bad_event(player_state)
    if not random_event:
        return
    else:
        player_state.apply_bad_event(random_event)
        update_player_state(player_state)

    return random_event