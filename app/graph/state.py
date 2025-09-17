from typing import TypedDict, Dict, Any

class GraphState(TypedDict):
    cv_text: str
    job_role: str
    structured_cv: Dict[str, Any]
    skill_analysis: Dict[str, Any]
    market_analysis: str
    final_report: str