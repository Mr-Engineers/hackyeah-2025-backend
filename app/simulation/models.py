# Możesz dodać modele zdarzeń symulacji, np. rok gry, losowe wydarzenia
from pydantic import BaseModel

class SimulationEvent(BaseModel):
    year_passed: int
    message: str
