from pydantic import BaseModel
from typing import Optional, Dict

class PlayerState(BaseModel):
    age: int = 18
    health: int = 100
    education: int = 0
    career_level: int = 0
    income: float = 0
    savings: float = 0.0
    happiness: int = 50
    social_relations: int = 50
    zus_balance: float = 0.0
    spendings: float = 0.0
    family: Dict[str, Optional[int]] = {"has_partner": 0, "children": 0}
