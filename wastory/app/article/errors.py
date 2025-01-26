from wastory.common.errors import WastoryHttpException


class ArticleNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Article not found")

class ArticleNotPublishedError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Article is not published")

class ArticleNotDraftError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Article is not draft, already Published")