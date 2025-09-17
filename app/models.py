from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    cv_text: str
    job_role: str

class AnalysisResponse(BaseModel):
    report: str