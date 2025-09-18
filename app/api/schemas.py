from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class AnalysisTextRequest(BaseModel):
    cv_text: str = Field(..., min_length=30, description="Candidate CV text")
    job_role: str = Field(..., min_length=3, description="Target job role")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cv_text": "Extensive background in software engineering, specializing in backend systems and distributed architecture...",
                "job_role": "Software Engineer",
            }
        }
    )

class ErrorResponse(BaseModel):
    detail: str
    
class Job(BaseModel):
    id: str
    status: str
    filename: Optional[str] = None

class BatchJobResponse(BaseModel):
    batch_id: str
    jobs: List[Job]

class JobResultResponse(Job):
    result: Optional[str] = None