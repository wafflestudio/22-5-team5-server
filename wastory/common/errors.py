from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class WapangHttpException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class InvalidFieldFormatError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Invalid field format")


class MissingRequiredFieldError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Missing required fields")