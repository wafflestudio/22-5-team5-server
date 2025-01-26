from wastory.common.errors import WastoryHttpException


class DraftNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Draft not found")

class NoAuthoriztionError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="It's secret.")
