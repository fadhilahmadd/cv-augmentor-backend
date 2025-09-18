import uuid
import io
import zipfile
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import AnalysisTextRequest, BatchJobResponse, Job, JobResultResponse
from app.db import crud, models
from app.db.database import get_db
from app.core.tasks import run_analysis_task

router = APIRouter()

@router.post("/analyze/text", response_model=Job, status_code=202)
async def analyze_text_cv(
    request: AnalysisTextRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    batch_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    filename = f"text_input_{job_id[:8]}.txt"

    await crud.create_job(db=db, job_id=job_id, batch_id=batch_id, filename=filename)

    background_tasks.add_task(run_analysis_task, job_id, request.cv_text, request.job_role, filename)

    return Job(id=job_id, status="pending", filename=filename)

@router.post("/analyze/batch", response_model=BatchJobResponse, status_code=202)
async def analyze_batch_cvs(
    background_tasks: BackgroundTasks,
    job_role: str = Form(...),
    cv_files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    batch_id = str(uuid.uuid4())
    response_jobs = []

    for cv_file in cv_files:
        if cv_file.content_type != "text/plain":
            raise HTTPException(status_code=400, detail=f"File '{cv_file.filename}' is not a .txt file.")

        job_id = str(uuid.uuid4())
        await crud.create_job(db=db, job_id=job_id, batch_id=batch_id, filename=cv_file.filename)
        cv_text = (await cv_file.read()).decode("utf-8")
        
        background_tasks.add_task(run_analysis_task, job_id, cv_text, job_role, cv_file.filename)
        response_jobs.append(Job(job_id=job_id, status="pending", filename=cv_file.filename))

    return BatchJobResponse(batch_id=batch_id, jobs=response_jobs)

@router.get("/analyze/status/{job_id}", response_model=JobResultResponse)
async def get_analysis_status(job_id: str, db: AsyncSession = Depends(get_db)):
    job = await crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job

@router.get("/analyze/results/all/{batch_id}")
async def download_all_batch_results(batch_id: str, db: AsyncSession = Depends(get_db)):
    completed_jobs = await crud.get_jobs_by_batch(db, batch_id)
    
    if not any(job.status == models.JobStatus.COMPLETED for job in completed_jobs):
        raise HTTPException(status_code=404, detail="No completed jobs found for this batch ID.")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for job in completed_jobs:
            if job.status == models.JobStatus.COMPLETED:
                filename = job.filename.replace(".txt", "_report.md")
                zip_file.writestr(filename, job.result)

    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=batch_{batch_id}_reports.zip"}
    )