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
        self._handle_investments(state, current_year)
        
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
                rates = {"UoP": 0.19, "UoD": 0.18, "B2B": 0.15}
                contribution = job.salary * rates.get(job.employment_type, 0.19)
                state.add_year_contribution(year=current_year, worked=True, contribution=contribution)
                state.zus_balance += contribution
                state.income = job.salary
                return
        # brak pracy w tym roku
        state.add_year_contribution(year=current_year, worked=False, contribution=0.0)
        state.income = 0

    def _update_savings(self, state: PlayerState):
        state.savings += max(0, state.income - state.spendings)

    def _handle_investments(self, state: PlayerState, current_year: int):
        state.process_investments(current_year=current_year)
