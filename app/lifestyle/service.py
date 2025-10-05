from sqlalchemy.ext.asyncio import AsyncSession
from ..player_state.router import service
from .model import LifestyleAction

class LifestyleService:
    async def get_action_by_id(self, db: AsyncSession, action_id: int) -> LifestyleAction | None:
        return await db.get(LifestyleAction, action_id)
    
    async def execute_action(self, db: AsyncSession, action_id: int):
        player_state = service.load_state()
        action = await self.get_action_by_id(db, action_id)

        if not action:
            raise ValueError("action not found")
        
        if player_state.savings < action.cost:
            raise ValueError("not enough money")
        
        player_state.savings -= action.cost

        for key, value in action.effects.items():
            if hasattr(player_state, key):
                current_value = getattr(player_state, key)
                setattr(player_state, key, current_value + value)
        service.save_state(player_state)
        return player_state