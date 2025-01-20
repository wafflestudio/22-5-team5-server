from wastory.common.errors import WastoryHttpException


class BlogNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Blog not found")

class CategoryNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Category not found")

class CategoryNameDuplicateError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=409, detail="Category name already exists")


class InvalidFieldFormatError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Invalid field format")


class MissingRequiredFieldError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Missing Required Field format")


class NotOwnerError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="User Not Allowed")