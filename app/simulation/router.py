from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.simulation.services import GameSimulator
from app.player_state.services import PlayerStateService
from app.simulation.schema import SimulationResponse
from app.career.repository import JobRepository
from app.database import get_db


db = get_db()
job_repo = JobRepository()
router = APIRouter()
player_service = PlayerStateService()
simulator = GameSimulator(player_service, job_repo)

@router.post("/game/next_year", response_model=SimulationResponse)
async def next_year(db: AsyncSession = Depends(get_db)):
    state = await simulator.next_year(db)
    return SimulationResponse(state=state, message=f"Rok przesunięty. Gracz ma teraz {state.age} lat.")
