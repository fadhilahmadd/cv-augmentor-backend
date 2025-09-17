from langchain_core.language_models.chat_models import BaseChatModel
from app.prompts.prompts import report_generator_prompt

def generate_report(state: dict, llm: BaseChatModel):

    job_role = state["job_role"]
    skill_analysis = state["skill_analysis"]
    market_analysis = state["market_analysis"]
    
    chain = report_generator_prompt | llm
    
    response = chain.invoke({
        "job_role": job_role,
        "skill_analysis": skill_analysis,
        "market_analysis": market_analysis
    })
    
    return {"final_report": response.content}