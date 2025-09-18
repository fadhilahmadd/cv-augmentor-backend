from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db import models

async def create_job(db: AsyncSession, job_id: str, batch_id: str, filename: str) -> models.Job:
    db_job = models.Job(id=job_id, batch_id=batch_id, filename=filename, status=models.JobStatus.PENDING)
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def get_job(db: AsyncSession, job_id: str) -> Optional[models.Job]:
    result = await db.execute(select(models.Job).filter(models.Job.id == job_id))
    return result.scalars().first()

async def get_jobs_by_batch(db: AsyncSession, batch_id: str) -> List[models.Job]:
    result = await db.execute(select(models.Job).filter(models.Job.batch_id == batch_id))
    return result.scalars().all()

async def update_job(db: AsyncSession, job_id: str, status: models.JobStatus, result: Optional[str] = None) -> Optional[models.Job]:
    job = await get_job(db, job_id)
    if job:
        job.status = status
        if result:
            job.result = result
        await db.commit()
        await db.refresh(job)
    return job