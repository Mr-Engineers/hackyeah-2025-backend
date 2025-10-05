from pydantic import BaseModel
from typing import Optional, Dict

class PlayerStateUpdate(BaseModel):
    age: Optional[int]
    sex: Optional[str]
    health: Optional[int]
    education: Optional[int]
    career_level: Optional[int]
    income: Optional[float]
    gross_income: Optional[float]
    savings: Optional[float]
    happiness: Optional[int]
    social_relations: Optional[int]
    zus_balance: Optional[float]
    spendings: Optional[float]
    family: Optional[Dict[str, Optional[int]]]
    job_id: Optional[int]
    lifestyle_expenses: Optional[int]
    investments: Optional[float]
    capital_initial: Optional[float]