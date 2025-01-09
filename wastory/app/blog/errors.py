from wastory.common.errors import WastoryHttpException


class BlognameAlreadyExistsError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Blogname already exists")

class BlogNotFoundError(WastoryHttpException):
    def __init__(self):
        super().__init__(status_code=404, detail="Blog not found")


class InvalidFieldFormatError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Invalid field format")


class MissingRequiredFieldError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Missing required fields")


class UserUnsignedError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail="User is not signed in")

class BlogAlreadyExistsError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Blog exists")