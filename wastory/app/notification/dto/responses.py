from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from wastory.app.notification.models import Notification

class NotificationResponse(BaseModel):
    id: int
    notification_type: int
    username: str
    blog_id: int
    blog_name: str
    blog_main_image_url: str | None
    article_id: int | None
    article_title: str | None
    comment_content: str | None
    created_at: datetime
    checked: bool = False

class NotificationListResponse(BaseModel):
    total_count: int
    notifications: List[NotificationResponse]

class PaginatedNotificationListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    notifications: List[NotificationResponse]