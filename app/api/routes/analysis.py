from fastapi import APIRouter
from app.api.schemas import AnalysisRequest, AnalysisResponse
from app.graph.workflow import graph_app
from app.core.exceptions import AIServiceException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analysis", response_model=AnalysisResponse)
async def analysis(request: AnalysisRequest):
    try:
        inputs = {"cv_text": request.cv_text, "job_role": request.job_role}
        final_state = await graph_app.ainvoke(inputs)
        report = final_state.get("final_report")

        if not report or not isinstance(report, str) or len(report.strip()) == 0:
            raise AIServiceException("AI model generated an empty or invalid report.")
            
        return AnalysisResponse(report=report)

    except Exception as e:
        raise AIServiceException(f"Failed to process CV with the AI model. Error: {e.__class__.__name__}")