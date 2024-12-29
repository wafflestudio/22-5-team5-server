from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from wastory.api import api_router
from wastory.common.errors import MissingRequiredFieldError
from wastory.database.middleware import DefaultSessionMiddleware

app = FastAPI()

app.include_router(api_router, prefix="/api")

app.add_middleware(DefaultSessionMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if isinstance(error, dict) and error.get("type", None) == "missing":
            raise MissingRequiredFieldError()
    return await request_validation_exception_handler(request, exc)