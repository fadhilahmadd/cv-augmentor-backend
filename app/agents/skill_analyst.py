from langchain_core.language_models.chat_models import BaseChatModel
from app.prompts.prompts import skill_analyst_prompt

def analyze_skills(state: dict, llm: BaseChatModel):
    structured_cv = state["structured_cv"]
    
    chain = skill_analyst_prompt | llm
    
    response = chain.invoke({"structured_cv": structured_cv})
    
    return {"skill_analysis": response.content}