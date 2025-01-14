from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND
)


class BlogNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "blog not found")

class CommentNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_404_NOT_FOUND, "category not found")

class CategoryNameDuplicateError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "category already exists")


class InvalidFieldFormatError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Invalid field format")


class MissingRequiredFieldError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_400_BAD_REQUEST, "Missing required fields")


class NotOwnerError(HTTPException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "category owner is not user")