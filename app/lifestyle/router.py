from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .service import LifestyleService
from ..player_state.schema import PlayerStateUpdate

router = APIRouter(prefix="/lifestyle")
lifestyle_service = LifestyleService()

@router.post("/execute/{action_id}", response_model=PlayerStateUpdate)
async def execute_lifestyle_action(action_id: int, db: AsyncSession = Depends(get_db)):
    try:
        updated_state = await lifestyle_service.execute_action(db, action_id)
        return updated_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
