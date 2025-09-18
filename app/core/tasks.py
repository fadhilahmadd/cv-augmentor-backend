from app.graph.workflow import graph_app
from app.db.database import AsyncSessionLocal
from app.db import crud, models
import logging

logger = logging.getLogger(__name__)

async def run_analysis_task(job_id: str, cv_text: str, job_role: str, filename: str):
    async with AsyncSessionLocal() as db:
        try:
            await crud.update_job(db=db, job_id=job_id, status=models.JobStatus.PROCESSING)

            inputs = {"cv_text": cv_text, "job_role": job_role}
            final_state = await graph_app.ainvoke(inputs)
            report = final_state.get("final_report")

            if not report:
                raise ValueError("Analysis failed to produce a report.")

            await crud.update_job(db=db, job_id=job_id, status=models.JobStatus.COMPLETED, result=report)

        except Exception as e:
            await crud.update_job(db=db, job_id=job_id, status=models.JobStatus.FAILED, result=str(e))