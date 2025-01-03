from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from wastory.api import api_router
from wastory.common.errors import MissingRequiredFieldError
from wastory.database.middleware import DefaultSessionMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Swift 앱 도메인을 추가 ("*": 모든 도메인 허용)
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메소드 ("*": 모든 메소드 허용)
    allow_headers=["*"],  # 허용할 헤더 ("*": 모든 헤더 허용)
)

app.include_router(api_router, prefix="/api")

app.add_middleware(DefaultSessionMiddleware)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.head("/")
async def head_root():
    return


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if isinstance(error, dict) and error.get("type", None) == "missing":
            raise MissingRequiredFieldError()
    return await request_validation_exception_handler(request, exc)