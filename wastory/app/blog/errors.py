from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)


class BlognameAlreadyExistsError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "Blogname already exists")

class Blog


class InvalidFieldFormatError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Invalid field format")


class MissingRequiredFieldError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Missing required fields")


class UserUnsignedError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "User is not signed in")