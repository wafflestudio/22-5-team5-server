from wastory.common.errors import WastoryHttpException


class S3ClientError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=500, detail="S3 Client Error")

class UnexpectedError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=500, detail="Unexpected Error")

class FileNotFoundError(WastoryHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="File Not Found")


