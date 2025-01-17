from datetime import datetime
from pydantic import BaseModel
from typing import List
from wastory.app.blog.dto.responses import BlogDetailResponse

class SubscriptionDetailResponse(BaseModel):
    id: int
    subscriber_id: int
    subscribed_id: int
    created_at: datetime  # datetime 타입으로 명시

    class Config:
        orm_mode = True

class PaginatedSubscriptionResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    blogs: List[BlogDetailResponse]
