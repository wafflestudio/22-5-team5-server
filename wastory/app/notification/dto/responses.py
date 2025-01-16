from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from wastory.app.notification.models import Notification

class NotificationResponse(BaseModel):
    id: int
    notification_type: int
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    checked: bool = False
    user_id : int
    @staticmethod
    def from_notification(notification: Notification) -> "NotificationResponse":
        return NotificationResponse(
            id=notification.id,
            notification_type=notification.notification_type,
            description=notification.description,
            created_at=notification.created_at,
            updated_at=notification.updated_at,
            checked=notification.checked,
            user_id=notification.user_id
        )

class NotificationListResponse(BaseModel):
    total_count: int
    notifications: List[NotificationResponse]