from pydantic import BaseModel, Field
from typing import List, Optional

class Family(BaseModel):
    has_partner: bool = False
    children_count: int = 0

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
    family: Family = Family()