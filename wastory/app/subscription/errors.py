from wastory.common.errors import WastoryHttpException


class SubscriptionAlreadyExistsError(WastoryHttpException):
    def __init__(self):
        super().__init__(status_code=400, detail="Subscription Already Exists")

class BlogNotFoundError(WastoryHttpException):
    def __init__(self):
        super().__init__(status_code=404, detail="Blog not found")

class SubscriptionNotFoundError(WastoryHttpException):
    def __init__(self):
        super().__init__(status_code=404, detail="Subscription not found")