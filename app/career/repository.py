from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Job

class JobRepository:
    async def get_by_id(self, db: AsyncSession, job_id: int) -> Job | None:
        return await db.get(Job, job_id)
    
    async def get_all(self, db: AsyncSession) -> list[Job]:
        stmt = select(Job)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_available_for_player(self, db: AsyncSession, education: int, experience: int) -> list[Job]:
        stmt = select(Job).where(
            Job.required_education <= education,
            Job.required_experience <= experience
        )
        result = await db.execute(stmt)
        return result.scalars().all()