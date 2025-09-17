from pydantic import BaseModel, Field
from langchain_core.language_models.chat_models import BaseChatModel
from app.prompts.prompts import cv_parser_prompt
from typing import List

class ExperienceItem(BaseModel):
    title: str = Field(description="The job title or role.")
    description: str = Field(description="A brief description of the responsibilities and achievements.")

class EducationItem(BaseModel):
    degree: str = Field(description="The degree or qualification obtained.")
    institution: str = Field(description="The name of the university or institution.")

class ProjectItem(BaseModel):
    title: str = Field(description="The name of the project.")
    description: str = Field(description="A brief description of the project.")

class StructuredCV(BaseModel):
    contact_info: dict = Field(description="Contact information like email and phone.")
    summary: str = Field(description="The professional summary or objective statement.")
    experience: List[ExperienceItem] = Field(description="A list of professional experiences.")
    education: List[EducationItem] = Field(description="A list of educational qualifications.")
    skills: List[str] = Field(description="A list of technical and soft skills.")
    projects: List[ProjectItem] = Field(description="A list of personal or professional projects.")

def parse_cv(state: dict, llm: BaseChatModel):
    cv_text = state["cv_text"]
    
    structured_llm = llm.with_structured_output(StructuredCV)
    chain = cv_parser_prompt | structured_llm
    response = chain.invoke({"cv_text": cv_text})
    
    return {"structured_cv": response.model_dump()}