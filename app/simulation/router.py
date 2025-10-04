from fastapi import APIRouter
from app.simulation.services import GameSimulator
from app.player_state.services import PlayerStateService
from app.simulation.schema import SimulationResponse
from app.career.repository import JobRepository


router = APIRouter()
player_service = PlayerStateService()
simulator = GameSimulator(player_service, JobRepository)

@router.post("/game/next_year", response_model=SimulationResponse)
def next_year():
    state = simulator.next_year()
    return SimulationResponse(state=state, message=f"Rok przesunięty. Gracz ma teraz {state.age} lat.")
