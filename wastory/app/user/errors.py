from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)
from wastory.common.errors import WastoryHttpException

class EmailAlreadyExistsError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail="Email already exists")


class UsernameAlreadyExistsError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail="Username already exists")


class InvalidFieldFormatError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Invalid field format")


class MissingRequiredFieldError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Missing required fields")


class UserUnsignedError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="User is not signed in")

class InvalidUsernameOrPasswordError(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Invalid username or password")

class ExpiredSignatureError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Token expired")

class InvalidTokenError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Invalid token")

class BlockedTokenError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="Blocked token")