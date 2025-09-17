from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError 
from dotenv import load_dotenv
from app.api.routes import analysis
from app.core.exceptions import (
    AIServiceException,
    ai_service_exception_handler,
    generic_exception_handler,
    request_validation_exception_handler
)

load_dotenv()

app = FastAPI(
    title="CV Augmentor API",
    description="An AI multi-agent system to analyze CVs and generate skill-gap reports.",
    version="1.0.0"
)

app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(AIServiceException, ai_service_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(analysis.router, prefix="/api", tags=["Analysis"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the CV Augmentor API"}