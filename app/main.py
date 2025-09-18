from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError 
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analysis
from app.core.config import ENVIRONMENT, ALLOWED_ORIGINS
from app.core.exceptions import (
    AIServiceException,
    ai_service_exception_handler,
    generic_exception_handler,
    request_validation_exception_handler
)
from app.db.database import engine, Base

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

docs_kwargs = {}
if ENVIRONMENT == "production":
    docs_kwargs["docs_url"] = None
    docs_kwargs["redoc_url"] = None

app = FastAPI(
    title="CV Augmentor API",
    description="An AI multi-agent system to analyze CVs and generate skill-gap reports.",
    version="1.0.0",
    **docs_kwargs
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", create_db_and_tables)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(AIServiceException, ai_service_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(analysis.router, prefix="/api", tags=["Analysis"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the CV Augmentor API"}