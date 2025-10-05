from app.player_state.services import PlayerStateService
from app.player_state.models import PlayerState
from app.career.repository import JobRepository
from sqlalchemy.ext.asyncio import AsyncSession
import random
from .health import health_calculator
from typing import Tuple

class GameSimulator:
    def __init__(self, player_service: PlayerStateService, job_repo: JobRepository):
        self.player_service = player_service
        self.job_repo = job_repo
        
        self.avg_monthly_wage = 8549.18
        self.pref_base = 1399.80
        self.full_base = 5203.80

    async def next_year(self, db: AsyncSession) -> PlayerState:
        state = self.player_service.load_state()
        
        self._increase_age(state)
        current_year = self._calculate_current_year(state)

        await self._add_yearly_contribution(state, current_year, db)
        self._update_savings(state)
        
        health_calculator.calculate_annual_change(state, state.job_id)

        state.update_zus_balance()
        self.player_service.save_state(state)

        self._calculate_yearly_return(state)
        return state

    def _increase_age(self, state: PlayerState):
        state.age += 1

    def _calculate_current_year(self, state: PlayerState) -> int:
        return len(state.zus_yearly_contributions) + 1

    async def _add_yearly_contribution(self, state: PlayerState, current_year: int, db: AsyncSession):

        if not state.job_id:
            state.add_year_contribution(year=current_year, worked=False, contribution=0.0)
            state.gross_income = 0.0
            state.income = 0.0
            return

        job = self.job_repo.get_by_id(db, state.job_id)
        if not job:
            state.add_year_contribution(year=current_year, worked=False, contribution=0.0)
            state.gross_income = 0.0
            state.income = 0.0
            return

        employment = job.employment_type
        monthly = float(job.salary or 0.0)
        gross_year = monthly * 12.0
        state.gross_income = gross_year

        if employment == "Umowa o prace":
            chorobowa = gross_year * 0.0245
            emerytalna = gross_year * 0.0976
            rentowa = gross_year * 0.015
            social_total = chorobowa + emerytalna + rentowa

            health = gross_year * 0.09

            tax = self._calculate_progressive_tax_for_employment(gross_year, social_total, state.age)
            net_income = gross_year - social_total - health - tax

            zus_contribution_yearly = gross_year * 0.1952
            state.add_year_contribution(year=current_year, worked=True, contribution=zus_contribution_yearly)
            state.income = max(0.0, net_income)

        # Umowa zlecenie
        elif employment == "Umowa zlecenie":
            is_student_under_26 = (state.age < 26 and gross_year <= 85528)
            if is_student_under_26:
                social_total = 0.0
                health = 0.0
            else:
                chorobowa = gross_year * 0.0245
                emerytalna = gross_year * 0.0976
                rentowa = gross_year * 0.015
                wypadkowe = gross_year * 0.0167  
                social_total = chorobowa + emerytalna + rentowa + wypadkowe
                health = gross_year * 0.09

            tax = self._calculate_progressive_tax_for_employment(gross_year, social_total, state.age)
            net_income = gross_year - social_total - health - tax

            zus_contribution_yearly = 0.0
            if not is_student_under_26:
                zus_contribution_yearly = gross_year * 0.1952

            state.add_year_contribution(year=current_year, worked=not is_student_under_26, contribution=zus_contribution_yearly)
            state.income = max(0.0, net_income)

        elif employment == "Umowa o dzielo" or employment == "Umowa o dzieło":
            # brak składek społecznych; podatek 20%
            tax = gross_year * 0.20
            net_income = gross_year - tax
            state.add_year_contribution(year=current_year, worked=False, contribution=0.0)
            state.income = max(0.0, net_income)

        elif employment in ["Kontrakt", "B2B", "Działalność gospodarcza"]:
            yearly_contribution, net_income = self._calculate_b2b_contributions_and_net(gross_year, state)
            state.add_year_contribution(year=current_year, worked=True if yearly_contribution > 0 else False, contribution=yearly_contribution)
            state.income = max(0.0, net_income)

            state.b2b_months_active += 12

        else:
            state.add_year_contribution(year=current_year, worked=False, contribution=0.0)
            state.income = gross_year

        state.update_zus_balance()

    def _calculate_progressive_tax_for_employment(self, gross_year: float, social_total: float, age: int) -> float:
        if age < 26 and gross_year <= 85528:
            return 0.0

        taxable = max(0.0, gross_year - social_total)
        allowance = 30000.0
        taxable_after_allowance = max(0.0, taxable - allowance)

        if taxable_after_allowance <= 120000.0:
            tax = taxable_after_allowance * 0.12
        else:
            tax = 120000.0 * 0.12 + (taxable_after_allowance - 120000.0) * 0.32

        return tax
    
    def _calculate_b2b_contributions_and_net(self, gross_year: float, state: PlayerState) -> Tuple[float, float]:

        months = state.b2b_months_active or 0

        if months < 6:
            social_yearly = 0.0
            used_base = 0.0
        elif months < 6 + 24:
            used_base = self.pref_base
            pension_m = used_base * 0.1952
            disability_m = used_base * 0.08
            accident_m = used_base * 0.0167
            sickness_m = used_base * 0.0245
            monthly_social = pension_m + disability_m + accident_m + sickness_m
            social_yearly = monthly_social * 12.0
        else:
            # pełny ZUS
            used_base = self.full_base
            pension_m = used_base * 0.1952
            disability_m = used_base * 0.08
            accident_m = used_base * 0.0167
            sickness_m = used_base * 0.0245
            monthly_social = pension_m + disability_m + accident_m + sickness_m
            social_yearly = monthly_social * 12.0

        avg = self.avg_monthly_wage
        if gross_year <= 60000.0:
            health_base_monthly = 0.6 * avg
        elif gross_year <= 300000.0:
            health_base_monthly = 1.0 * avg
        else:
            health_base_monthly = 1.8 * avg
        health_yearly = health_base_monthly * 0.09 * 12.0

        tax = gross_year * 0.12

        net_income = gross_year - social_yearly - health_yearly - tax

        yearly_contribution_value = social_yearly 
        return yearly_contribution_value, max(0.0, net_income)
    
    def _update_savings(self, state: PlayerState):
        state.savings += max(0, state.income - state.spendings)

    def _calculate_yearly_return(self, state: PlayerState) -> float:
        if state.investments > 0:
            return_rate = random.uniform(-1.04, 1.1)
            growth = state.investments * return_rate
            state.investments += growth

            self.player_service.save_state(state)
            return return_rate
        return 0
    
