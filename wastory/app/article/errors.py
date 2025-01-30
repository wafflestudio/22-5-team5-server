from wastory.common.errors import WastoryHttpException


class ArticleNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Article not found")

class NoAuthoriztionError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="It's secret.")

class MissingPassword(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Password is missing")
