from typing import Annotated

from fastapi import Depends
from wastory.app.notification.models import Notification
from wastory.app.user.models import User
from wastory.app.notification.store import NotificationStore
from wastory.app.notification.dto.responses import NotificationResponse
from wastory.app.notification.errors import NotificationNotFoundError
from wastory.app.user.service import UserStore


class NotificationService:
    def __init__(self, notification_store: Annotated[NotificationStore, Depends()], user_store: Annotated[UserStore, Depends()]) -> None:
        self.notification_store = notification_store
        self.user_store = user_store

    # async def create_notification(
    #     self,
    #     user : User,
    #     type : int,
    # ):
        
    #     notification = await self.notification_store.add_notification(user_id=user.id, type=type)

    #     return NotificationResponse(notification)
    
    async def get_notification_by_id(self, notification_id : int) -> NotificationResponse:
        notification=await self.notification_store.get_notification_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError
        return NotificationResponse.from_notification(notification)
    
    async def get_notifications_by_user(self, user : User) -> list[Notification] | None:
        notifications = await self.notification_store.get_notifications_of_user(user.id)
        if notifications is None:
            raise NotificationNotFoundError
        return notifications

    async def delete_notification_by_id(self, notification_id: int) -> None:
        notification = await self.notification_store.get_notification_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError
        await self.notification_store.delete_notification(notification)

    async def check_notification(self, notification_id : int) -> None:
        notification = await self.notification_store.get_notification_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError
        await self.notification_store.check_notification(notification)