from sqlalchemy.ext.asyncio import AsyncSession
from ..player_state.router import service
from .model import LifestyleAction
from ..core.game_data import game_data

class LifestyleService:
    def get_action_by_id(self, action_id: int) -> LifestyleAction | None:
        for action in game_data.lifestyle_actions:
            if action.id == action_id:
                return action
        return None
    
    async def execute_action(self, action_id: int):
        player_state = service.load_state()
        action = self.get_action_by_id(action_id)

        if not action:
            raise ValueError("action not found")
        
        if player_state.savings < action.cost:
            raise ValueError("not enough money")
        
        player_state.savings -= action.cost

        for key, value in action.effects.items():
            if hasattr(player_state, key):
                current_value = getattr(player_state, key)
                new_value = current_value + value
                if key in STAT_CAPS:
                    new_value = min(new_value, STAT_CAPS[key])
                setattr(player_state, key, new_value)
        player_state.lifestyle_expenses += action.cost
        service.save_state(player_state)

        return player_state
    

STAT_CAPS = {
    "health": 1000,
    "happiness": 1000,
    "social_relations": 1000,
    "education": 5 
}