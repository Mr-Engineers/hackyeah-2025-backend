from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from . import schema
from .service import CareerService, JobNotFoundError, PlayerNotQualifiedError
from ..player_state.models import PlayerState as PlayerStateSchema

router = APIRouter(prefix="/career")
career_service = CareerService()

@router.get("/job_offers", response_model=List[schema.JobOffer])
async def get_job_offers(db: AsyncSession = Depends(get_db)):
    offers = await career_service.get_random_job_offers(db)
    return offers

@router.post("/apply", response_model=PlayerStateSchema)
async def apply_for_job(request: schema.JobApplyRequest, db: AsyncSession = Depends(get_db)):
    try:
        updated_player_state = await career_service.apply_for_job(
            db, job_id=request.job_id
        )
        return updated_player_state
    except JobNotFoundError as e :
        raise HTTPException(status_code=404, detial=str(e))
    except PlayerNotQualifiedError(e):
        raise HTTPException(status_code=400, detail=str(e))
    
    