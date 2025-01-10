from wastory.common.errors import WastoryHttpException


class ArticleNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Item not found")
