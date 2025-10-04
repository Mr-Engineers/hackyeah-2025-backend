from pydantic import BaseModel
from typing import Optional, Dict, List

class YearContribution(BaseModel):
    year: int
    worked: bool = True
    contribution: float = 0.0

class PlayerState(BaseModel):
    age: int = 18
    sex: str = "Mężczyzna"
    health: int = 100
    education: int = 0
    career_level: int = 0
    income: float = 0
    savings: float = 0.0
    happiness: int = 50
    social_relations: int = 50
    zus_balance: float = 0.0
    spendings: float = 0.0
    job_id: Optional[int] = None
    
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
    
    def add_contribution(self, year: int, contract_type: str, base_salary: float):
        """
        contract_type: "UoP", "UoD", "B2B"
        base_salary: wynagrodzenie w danym roku
        """
        # przykładowe stawki składek
        rates = {"UoP": 0.19, "UoD": 0.18, "B2B": 0.15}
        contribution = base_salary * rates.get(contract_type, 0.19)
        self.zus_yearly_contributions.append(
            YearContribution(year=year, worked=True, contribution=contribution)
        )
        self.zus_balance += contribution

