from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from .model import Job

class JobRepository:
    async def get_by_id(self, db: AsyncSession, job_id: int) -> Job | None:
        return await db.get(Job, job_id)
    
    async def get_all(self, db: AsyncSession) -> list[Job]:
        stmt = select(Job)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_random_jobs(self, db: AsyncSession, limit: int) -> list[Job]:
        stmt = select(Job).order_by(func.random()).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_by_title_and_tier(self, db: AsyncSession, title: str, tier: int) -> Job | None:
        stmt = select(Job).where(
            Job.title == title,
            Job.tier == tier
        )
        result = await db.execute(stmt)
        return result.scalars().first()