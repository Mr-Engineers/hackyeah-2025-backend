from typing import Optional
from ..career.model import Job
from ..player_state.models import PlayerState
from ..player_state.router import service
from ..career.repository import job_repo
from sqlalchemy.ext.asyncio import AsyncSession

class HealthCalculator:
    def calculate_annual_change(self, player: PlayerState, job_id: Optional[int], db: AsyncSession) -> PlayerState:
        total_change = 0
        if 18 <= player.age <= 30:
            total_change -= 2
        elif 31 <= player.age <= 45:
            total_change -= 5
        elif 46 <= player.age <= 60:
            total_change -= 10
        else:
            total_change -= 20

        if job_id:
            job = job_repo.get_by_id(db, job_id)
            stress_penalty = job.stress_level * 1.5
            total_change -= stress_penalty

        player.health += total_change
        service.save_state(player)
        return player

health_calculator = HealthCalculator()