from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)


class EmailAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "Email already exists")


class UsernameAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "Username already exists")


class InvalidFieldFormatError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Invalid field format")


class MissingRequiredFieldError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Missing required fields")


class UserUnsignedError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "User is not signed in")