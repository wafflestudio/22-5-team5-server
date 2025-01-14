from typing import Annotated, List

from fastapi import Depends
from wastory.app.notification.models import Notification
from wastory.app.user.models import User
from wastory.app.blog.models import Blog
from wastory.app.notification.store import NotificationStore
from wastory.app.notification.dto.responses import NotificationResponse
from wastory.app.notification.errors import NotificationNotFoundError
from wastory.app.user.service import UserStore
from wastory.app.blog.service import BlogStore


class NotificationService:
    def __init__(
            self,
            notification_store: Annotated[NotificationStore, Depends()],
            user_store: Annotated[UserStore, Depends()],
            blog_store: Annotated[BlogStore, Depends()]
            ) -> None:
        self.notification_store = notification_store
        self.user_store = user_store
        self.blog_store = blog_store

    async def add_notification(
        self,
        blog_address_names : List[str],
        type : int,
        description : str | None,
    ) -> None:
        print("address_name", blog_address_names)
        blogs = [
            await self.blog_store.get_blog_by_address_name(address_name)
            for address_name in blog_address_names
        ]
        user_ids = [blog.user_id for blog in blogs]
        print(user_ids)
        await self.notification_store.add_notification(user_ids=user_ids, type=type, description=description)
    
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

    async def delete_notification_by_id(self, user : User, notification_id: int) -> None:
        notification = await self.notification_store.get_notification_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError
        if notification.user_id is not user.id:
            raise NotificationNotFoundError
        await self.notification_store.delete_notification(notification_id)

    async def check_notification(self, user : User, notification_id : int) -> None:
        notification = await self.notification_store.get_notification_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError
        if notification.user_id is not user.id:
            raise NotificationNotFoundError
        await self.notification_store.check_notification(notification)