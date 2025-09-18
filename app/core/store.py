import uuid
from typing import Dict, Any

JOB_STORE: Dict[str, Dict[str, Any]] = {}

def create_job(batch_id: str):
    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = {
        "status": "pending",
        "result": None,
        "batch_id": batch_id,
        "filename": None
    }
    return job_id

def get_job(job_id: str):
    return JOB_STORE.get(job_id)

def update_job_status(job_id: str, status: str, result: str = None, filename: str = None):
    if job_id in JOB_STORE:
        JOB_STORE[job_id]["status"] = status
        if result:
            JOB_STORE[job_id]["result"] = result
        if filename:
            JOB_STORE[job_id]["filename"] = filename