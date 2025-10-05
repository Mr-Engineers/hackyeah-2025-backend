from pydantic import BaseModel
from typing import Dict, Any

class LifestyleActionRead(BaseModel):
    id: int
    name: str
    description: str
    cost: float
    effects: Dict[str, Any]
    requirements: Dict[str, Any]

    class Config:
        from_atrributes = True