from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from wastory.app.notification.models import Notification

class NotificationResponse(BaseModel):
    id: int
    notification_type: int
    notification_title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    checked: bool = False
    username: str
    blog_main_image_url: str | None

class NotificationListResponse(BaseModel):
    total_count: int
    notifications: List[NotificationResponse]

class PaginatedNotificationListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    notifications: List[NotificationResponse]