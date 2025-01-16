from wastory.common.errors import WastoryHttpException


class LikeNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Like not found")

class LikeAlreadyExistsError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Like Already Exists")