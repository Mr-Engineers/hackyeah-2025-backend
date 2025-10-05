from pydantic import BaseModel
from typing import Optional, Dict, List
from app.events.models import BadEvent

class YearContribution(BaseModel):
    year: int
    worked: bool = True
    contribution: float = 0.0

class PlayerState(BaseModel):
    age: int = 20
    sex: str = "Mężczyzna"
    health: int = 100
    education: int = 0
    career_level: int = 0
    income: float = 0.0 # netto rocznie po obliczeniach w symulacji
    gross_income: float = 0.0 # surowe roczne przychody (np. job.salary*12) - pomocnicze
    savings: float = 0.0
    happiness: int = 50
    social_relations: int = 50
    zus_balance: float = 0.0
    spendings: float = 0.0
    job_id: Optional[int] = None
    lifestyle_expenses: int = 0
    b2b_months_active: int = 0
    family: Dict[str, Optional[int]] = {"has_partner": 0, "children": 0}
    zus_yearly_contributions: List[YearContribution] = []
    investments: float = 0.0
    capital_initial: float = 0.0
    
    def add_year_contribution(self, year: int, worked: bool, contribution: float):
        self.zus_yearly_contributions.append(
            YearContribution(year=year, worked=worked, contribution=contribution)
        )
        
    def update_zus_balance(self):
        """Sumuje wszystkie składki roczne, aby uzyskać aktualne saldo ZUS"""
        self.zus_balance = sum(yc.contribution for yc in self.zus_yearly_contributions)
        

    def calculate_pension(self, expected_lifetime_months: int) -> float:
        total_contributions = sum(
            yc.contribution for yc in self.zus_yearly_contributions if yc.worked
        )
        total_contributions += self.capital_initial
        if expected_lifetime_months <= 0:
            raise ValueError("Expected lifetime months must be positive")
        return total_contributions / expected_lifetime_months
    
    def apply_bad_event(self, bad_event: BadEvent):
        changes_dict = bad_event.get_decreased_attribute_dict()
        for key, changed_value in changes_dict.items():
            current_value = getattr(self, key) 
            setattr(self, key, current_value - changed_value)
    
