from wastory.common.errors import WastoryHttpException


class MessageNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Message not found")


class UnauthorizedMessageAccessError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=403, detail="Unauthorized access to this message")
