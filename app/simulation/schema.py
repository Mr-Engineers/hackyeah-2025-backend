from pydantic import BaseModel
from app.player_state.models import PlayerState

class SimulationResponse(BaseModel):
    state: PlayerState
    message: str
