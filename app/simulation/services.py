from app.player_state.services import PlayerStateService
from app.player_state.models import PlayerState
from app.career.repository import JobRepository
from sqlalchemy.ext.asyncio import AsyncSession

class GameSimulator:
    def __init__(self, player_service: PlayerStateService, job_repo: JobRepository):
        self.player_service = player_service
        self.job_repo = job_repo

    async def next_year(self, db: AsyncSession) -> PlayerState:
        """Przechodzi do kolejnego roku symulacji"""
        state = self.player_service.load_state()
        
        self._increase_age(state)
        current_year = self._calculate_current_year(state)

        await self._add_yearly_contribution(state, current_year, db)
        self._update_savings(state)
        
        self.player_service.save_state(state)
        return state

    # --- Funkcje pomocnicze ---
    def _increase_age(self, state: PlayerState):
        state.age += 1

    def _calculate_current_year(self, state: PlayerState) -> int:
        return len(state.zus_yearly_contributions) + 1

    async def _add_yearly_contribution(self, state: PlayerState, current_year: int, db: AsyncSession):
        """Dodaje składkę do ZUS na podstawie job_id"""
        if state.job_id:
            job = await self.job_repo.get_by_id(db, state.job_id)
            if job:
                rates = {"Umowa o prace": 0.19, "Umowa o dzielo": 0.18, "Kontrakt": 0.15, "Umowa zlecenie": 0.1}
                contribution = job.salary*12 * rates.get(job.employment_type)
                state.add_year_contribution(year=current_year, worked=True, contribution=contribution)
                state.zus_balance += contribution
                state.income = job.salary*12
                return
        else:
            state.add_year_contribution(year=current_year, worked=False, contribution=0.0)
            state.income = 0
        state.update_zus_balance()

    def _update_savings(self, state: PlayerState):
        state.savings += max(0, state.income - state.spendings)
