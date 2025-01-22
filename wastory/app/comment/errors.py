from wastory.common.errors import WastoryHttpException


class BlogNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="blog not found")

class CommentNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404,detail= "comment not found")

class ParentOtherSectionError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=409,detail= "parent와 children 위치가 다릅니다")


class InvalidFieldFormatError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400,detail= "Invalid field format")

class InvalidLevelError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400,detail= "parent_should be level 1")

class MissingRequiredFieldError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400,detail= "Missing required fields")


class NotOwnerError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=401,detail= "User Not Allowed")