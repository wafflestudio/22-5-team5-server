from typing import List
from pydantic import BaseModel
from datetime import datetime
from wastory.app.message.models import Message


class MessageDetailResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    sender_id: int
    recipient_id: int
    is_read: bool

    @staticmethod
    def from_message(message: Message) -> "MessageDetailResponse":
        return MessageDetailResponse(
            id=message.id,
            content=message.content,
            created_at=message.created_at,
            updated_at=message.updated_at,
            sender_id=message.sender_id,
            recipient_id=message.recipient_id,
            is_read=message.is_read,
        )


class PaginatedMessageListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    messages: List[MessageDetailResponse]
