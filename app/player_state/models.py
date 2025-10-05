from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from app.events.models import BadEvent, Event

class YearContribution(BaseModel):
    year: int
    worked: bool = True
    contribution: float = 0.0

class PlayerState(BaseModel):
    age: int = 18
    sex: str = "Mężczyzna"
    health: int = Field(default=1000, ge=0, le=1000)
    education: int = Field(default=1, ge=1, le=5)
    career_level: int = Field(default=0, ge=0, le=1000)
    income: float = 0.0 # netto rocznie po obliczeniach w symulacji
    gross_income: float = 0.0 # surowe roczne przychody (np. job.salary*12) - pomocnicze
    savings: float = 0.0
    happiness: int = Field(default=500, ge=0, le=1000)
    social_relations: int = Field(default=500, ge=0, le=1000)
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
        

    def calculate_pension(self) -> float:
        total_contributions = sum(
            yc.contribution for yc in self.zus_yearly_contributions if yc.worked
        )
        total_contributions += self.capital_initial
        if self.age < 30:
            raise ValueError("nie mozesz przejsc na emeryture przed 30 rokiem zycia")
        return total_contributions / retirement_months_dict[self.age]
    
    def apply_bad_event(self, bad_event: BadEvent):
        changes_dict = bad_event.get_decreased_attribute_dict()
        for key, changed_value in changes_dict.items():
            current_value = getattr(self, key) 
            setattr(self, key, current_value - changed_value)

    def apply_event(self, event: Event):
        buffs = event.get_advantaged_attributes_dict()
        for key, changed_value in buffs.items():
            current_value = getattr(self, key) 
            setattr(self, key, current_value + changed_value)

        nerfs = event.get_disadvantaged_attributes_dict()
        for key, changed_value in nerfs.items():
            current_value = getattr(self, key) 
            setattr(self, key, current_value - changed_value)

retirement_months_dict = {
    30: 588.7,
    31: 577.2,
    32: 565.7,
    33: 554.2,
    34: 542.8,
    35: 531.4,
    36: 520.0,
    37: 508.7,
    38: 497.3,
    39: 486.1,
    40: 474.8,
    41: 463.7,
    42: 452.4,
    43: 441.4,
    44: 430.2,
    45: 419.3,
    46: 408.2,
    47: 397.3,
    48: 386.5,
    49: 375.7,
    50: 365.2,
    51: 354.6,
    52: 344.0,
    53: 333.7,
    54: 323.4,
    55: 313.2,
    56: 303.2,
    57: 293.3,
    58: 283.4,
    59: 273.7,
    60: 264.2,
    61: 254.9,
    62: 245.6,
    63: 236.5,
    64: 227.6,
    65: 218.9,
}