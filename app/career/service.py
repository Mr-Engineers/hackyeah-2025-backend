from sqlalchemy.ext.asyncio import AsyncSession
from .repository import JobRepository
from ..player_state.models import PlayerState
from ..player_state.services import PlayerStateService
from .schema import JobOffer

class CareerError(Exception):
    pass
class JobNotFoundError(CareerError):
    pass
class PlayerNotQualifiedError(CareerError):
    pass

class CareerService:
    def __init__(self):
        self.job_repo = JobRepository()
        self.player_state_service = PlayerStateService()
    
    async def get_random_job_offers(self, db: AsyncSession, game_id: int) -> list:
        player_state = self.player_state_service.load_state()
        random_jobs = await self.job_repo.get_random_jobs(db, limit=3)
        job_offers = []
        for job in random_jobs:
            is_eligible = (
                player_state.education >= job.required_education and
                player_state.career_level >= job.required_career_level
            )
            offer = JobOffer(
                job_details=job,
                eligible=is_eligible
            )
            job_offers.append(offer)

        return job_offers
    
    async def apply_for_job(self, db: AsyncSession, job_id: int) -> None:
        player_state = self.player_state_service.load_state()
        job = await self.job_repo.get_by_id(db, job_id)
        if not job:
            raise JobNotFoundError(f"praca o ID {job_id} nie zostala znaleziona")
        if player_state.education < job.required_education:
            raise PlayerNotQualifiedError("Gracz ma zbyt niski poziom edukacji.")
        if player_state.career_level < job.required_career_lebel:
            raise PlayerNotQualifiedError("Gracz ma zbyt niski poziom doświadczenia zawodowego.")
        
        player_state.job_id = job.id
        self.player_state_service.save_state(player_state)

        return player_state
    
    async def promotion_event(self, db: AsyncSession, game_id: int) -> bool:
        player_state = self.player_state_service.load_state()
        if not player_state or not player_state.job_id:
            return False
        current_job = await self.job_repo.get_by_id(db, player_state.job_id)
        if not current_job:
            return False
        next_tier = current_job.tier + 1
        next_job = await self.job_repo.find_job_by_title_and_tier(
            db,
            title=current_job.title,
            tier=next_tier
        )
        if not next_job:
            return False
        player_state.job_id = next_job.id
        self.player_state_service.save_state(player_state)
        return True
    
    async def promotion(self, db: AsyncSession, game_id: int) -> bool:
        player_state = self.player_state_service.load_state()
        if not player_state or not player_state.job_id:
            return False
        current_job = await self.job_repo.get_by_id(db, player_state.job_id)
        if not current_job:
            return False
        next_tier = current_job.tier + 1
        next_job = await self.job_repo.find_job_by_title_and_tier(
            db,
            title=current_job.title,
            tier=next_tier
        )
        if not next_job or player_state.career_level < next_job.requried_career_level:
            return False
        player_state.job_id = next_job.id
        self.player_state_service.save_state(player_state)
        return True