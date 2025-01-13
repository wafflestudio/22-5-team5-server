from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wastory.app.blog.errors import (
    BlogNotFoundError,
    BlognameAlreadyExistsError
)
from wastory.app.notification.models import Notification
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION


class NotificationStore:
    @transactional
    async def add_notification(self, user_id: int, type : int, description: str) -> Notification:
        description = "알림"
        if type == 1:
            description = ""
        notification=Notification(
            notification_type=type,
            description=description,
            user_id=user_id
        )
        SESSION.add(notification)
        await SESSION.flush()
        await SESSION.refresh(notification)
        return notification
    

    async def get_notification_by_id(self, notification_id: int) -> Notification | None:
        return await SESSION.scalar(select(Notification).where(Notification.id == notification_id))


    async def get_notifications_of_user(self, user_id: int) -> list[Notification] | None:
        notifications = await SESSION.execute(select(Notification).where(Notification.user_id == user_id))
        return notifications.scalars().all()


    @transactional
    async def delete_notification(self, notification: Notification) -> None:
        await SESSION.delete(notification)


    @transactional
    async def check_notification(self, notification: Notification) -> Notification:
        if notification.checked == True:
            return notification
        notification.checked = True

        return notification