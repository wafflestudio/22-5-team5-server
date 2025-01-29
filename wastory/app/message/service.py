from typing import Annotated, List

from fastapi import Depends
from wastory.app.message.store import MessageStore
from wastory.app.message.dto.responses import MessageDetailResponse, PaginatedMessageListResponse
from wastory.app.message.errors import MessageNotFoundError, UnauthorizedMessageAccessError
from wastory.app.user.service import UserService
from wastory.app.blog.service import BlogService
from wastory.app.notification.service import NotificationService


class MessageService:
    def __init__(
        self,
        message_store: Annotated[MessageStore, Depends()],
        user_service: Annotated[UserService, Depends()],
        blog_service: Annotated[BlogService, Depends()],
        notification_service: Annotated[NotificationService, Depends()],
    ) -> None:
        self.message_store = message_store
        self.user_service = user_service
        self.blog_service = blog_service
        self.notification_service = notification_service

    async def create_message(
        self, sender_id: int, recipient_id: int, content: str
    ) -> MessageDetailResponse:
        message = await self.message_store.create_message(
            sender_id=sender_id, recipient_id=recipient_id, content=content
        )
        sender = await self.user_service.get_user_by_id(sender_id)
        sender_blog = await self.blog_service.get_blog_by_user(sender)
        # 쪽지 알림
        await self.notification_service.add_notification(
            blog_address_names = [sender_blog.address_name],
            type = 5,
            notification_blog_name=sender_blog.blog_name,
            notification_blog_image_url=sender_blog.main_image_url
        )

        return MessageDetailResponse.from_message(message)

    async def get_received_messages(
        self, user_id: int, page: int, per_page: int
    ) -> PaginatedMessageListResponse:
        messages, total_count = await self.message_store.get_received_messages(
            recipient_id=user_id, page=page, per_page=per_page
        )
        message_ids = [msg.id for msg in messages if not msg.is_read]
        if message_ids:
            await self.message_store.mark_messages_as_read(user_id, message_ids)

        return PaginatedMessageListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            messages=[
                MessageDetailResponse.from_message(message) for message in messages
            ],
        )

    async def get_sent_messages(
        self, user_id: int, page: int, per_page: int
    ) -> PaginatedMessageListResponse:
        messages, total_count = await self.message_store.get_sent_messages(
            sender_id=user_id, page=page, per_page=per_page
        )
        return PaginatedMessageListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            messages=[
                MessageDetailResponse.from_message(message) for message in messages
            ],
        )

    async def get_message(self, user_id: int, message_id: int) -> MessageDetailResponse:
        message = await self.message_store.get_message_by_id(message_id)
        if not message or (message.sender_id != user_id and message.recipient_id != user_id):
            raise MessageNotFoundError()
        if message.recipient_id == user_id and not message.is_read:
            await self.message_store.mark_message_as_read(message_id)
        return MessageDetailResponse.from_message(message)

    async def delete_message(self, user_id: int, message_id: int) -> None:
        message = await self.message_store.get_message_by_id(message_id)
        if not message or (message.sender_id != user_id and message.recipient_id != user_id):
            raise MessageNotFoundError()
        if message.sender_id != user_id:
            raise UnauthorizedMessageAccessError()
        await self.message_store.soft_delete_message(message_id)
