from typing import List, Tuple
from sqlalchemy import select, func, desc

from wastory.app.message.models import Message
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION


class MessageStore:
    @transactional
    async def create_message(
        self, sender_id: int, recipient_id: int, content: str
    ) -> Message:
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
        )
        SESSION.add(message)
        await SESSION.flush()
        await SESSION.refresh(message)
        return message

    async def get_message_by_id(self, message_id: int) -> Message | None:
        query = select(Message).where(Message.id == message_id)
        message = await SESSION.scalar(query)
        return message

    async def get_received_messages(
        self, recipient_id: int, page: int, per_page: int
    ) -> Tuple[List[Message], int]:
        offset_val = (page - 1) * per_page
        query = (
            select(Message)
            .where(Message.recipient_id == recipient_id)
            .order_by(desc(Message.created_at))
            .offset(offset_val)
            .limit(per_page)
        )
        messages = await SESSION.scalars(query)
        count_query = select(func.count(Message.id)).where(Message.recipient_id == recipient_id)
        total_count = await SESSION.scalar(count_query)
        return list(messages), total_count or 0

    async def get_sent_messages(
        self, sender_id: int, page: int, per_page: int
    ) -> Tuple[List[Message], int]:
        offset_val = (page - 1) * per_page
        query = (
            select(Message)
            .where(Message.sender_id == sender_id)
            .order_by(desc(Message.created_at))
            .offset(offset_val)
            .limit(per_page)
        )
        messages = await SESSION.scalars(query)
        count_query = select(func.count(Message.id)).where(Message.sender_id == sender_id)
        total_count = await SESSION.scalar(count_query)
        return list(messages), total_count or 0

    @transactional
    async def mark_message_as_read(self, message_id: int) -> None:
        message = await self.get_message_by_id(message_id)
        if message:
            message.is_read = True
            SESSION.merge(message)
            await SESSION.flush()

    @transactional
    async def mark_messages_as_read(self, recipient_id: int, message_ids: List[int]) -> None:
        query = (
            select(Message)
            .where(Message.id.in_(message_ids), Message.recipient_id == recipient_id, Message.is_read == False)
        )
        messages = await SESSION.scalars(query)

        for message in messages:
            message.is_read = True

        await SESSION.flush()

    @transactional
    async def delete_message(self, message_id: int) -> None:
        message = await self.get_message_by_id(message_id)
        if message:
            await SESSION.delete(message)
            await SESSION.flush()

    @transactional
    async def soft_delete_message(self, message_id: int) -> None:
        message = await self.get_message_by_id(message_id)

        message.content = "삭제된 메시지입니다"

        SESSION.merge(message)
        await SESSION.flush()
