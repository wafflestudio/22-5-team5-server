from typing import Annotated, List, Optional

from fastapi import Depends
from wastory.app.notification.models import Notification
from wastory.app.user.models import User
from wastory.app.blog.models import Blog
from wastory.app.notification.store import NotificationStore
from wastory.app.notification.dto.responses import NotificationResponse, PaginatedNotificationListResponse
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
        username : str,
        type : int,
        notification_blog_name : str,
        notification_blog_image_url : str,
        article_id : int | None = None,
        comment_id : int | None = None,
    ) -> None:
        blogs = [
            await self.blog_store.get_blog_by_address_name(address_name)
            for address_name in blog_address_names
        ]
        notification_blog = await self.blog_store.get_blog_by_name(notification_blog_name)
        ids = [(blog.user_id, notification_blog.id, article_id, comment_id) for blog in blogs if blog is not None]
        await self.notification_store.add_notification(
            ids=ids, type=type, notification_blogname=notification_blog_name, notification_blog_image_url=notification_blog_image_url, username=username
            )
    
    async def get_notification_by_id(self, notification_id : int) -> NotificationResponse:
        notification=await self.notification_store.get_notification_by_id(notification_id)
        if notification is None:
            raise NotificationNotFoundError
        return NotificationResponse.from_notification(notification)

    async def get_notifications_by_user(self, user : User, page : int, per_page : int, type : Optional[int] = None) -> PaginatedNotificationListResponse:
        notifications = await self.notification_store.get_notifications_of_user(user.id, page, per_page, type)
        if notifications is None:
            raise NotificationNotFoundError
        return notifications
    
    # async def get_notifications_by_user(self, user : User) -> list[Notification] | None:
    #     notifications = await self.notification_store.get_notifications_of_user(user.id)
    #     if notifications is None:
    #         raise NotificationNotFoundError
    #     return notifications

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