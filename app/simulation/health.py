from typing import Optional
from ..career.model import Job
from ..player_state.models import PlayerState

class HealthCalculator:
    def calculate_annual_change(self, player: PlayerState, job: Optional[Job]) -> int:
        total_chage = 0
        if 18 <= player.age <= 30:
            total_chage -= 2
        elif 31 <= player.age <= 45:
            total_change -= 5
        elif 46 <= player.age <= 60:
            total_change -= 10
        else:
            total_change -= 20

        if job:
            stress_penalty = job.stress_level * 1.5
            total_change -= stress_penalty

        return total_change

        