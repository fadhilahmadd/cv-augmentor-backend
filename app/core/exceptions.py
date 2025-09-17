from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class AIServiceException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

async def ai_service_exception_handler(request: Request, exc: AIServiceException):
    return JSONResponse(
        status_code=503,
        content={"detail": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal error occurred. Please try again later."},
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = {}
    for error in exc.errors():
        field = error["loc"][-1] 
        message = error["msg"]
        error_messages[field] = message.capitalize()

    logger.warning(f"Request validation failed: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )