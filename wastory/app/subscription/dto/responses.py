from datetime import datetime
from pydantic import BaseModel

class SubscriptionDetailResponse(BaseModel):
    id: int
    subscriber_id: int
    subscribed_id: int
    created_at: datetime  # datetime 타입으로 명시

    class Config:
        orm_mode = True
