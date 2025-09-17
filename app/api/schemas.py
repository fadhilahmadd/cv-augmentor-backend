from pydantic import BaseModel, Field, ConfigDict

class AnalysisRequest(BaseModel):
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

class AnalysisResponse(BaseModel):
    report: str

class ErrorResponse(BaseModel):
    detail: str