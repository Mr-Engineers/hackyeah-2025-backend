import json
from ..lifestyle.schema import LifestyleActionRead
from typing import Type
from pydantic import BaseModel

class GameData:
    def __init__(self):
        self.lifestyle_actions: list[LifestyleActionRead]=self._load_data(
            path="app/core/data/lifestyle_actions.json",
            model=LifestyleActionRead
        )

    def _load_data(self, path: str, model: Type[BaseModel]):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [model.model_validate(item) for item in data]
    
game_data = GameData()