from typing import Self
from pydantic import BaseModel
from datetime import datetime
from wastory.app.like.models import Like


class LikeDetailResponse(BaseModel):
    id : int
    created_at: datetime

    @staticmethod
    def from_like(like: Like) -> "LikeDetailResponse":
        return LikeDetailResponse(
            id=like.id, created_at=like.created_at
        )


class LikeDetailInListResponse(BaseModel):
    id : int
    created_at: datetime

    @staticmethod
    def from_like(like: Like) -> "LikeDetailInListResponse":
        return LikeDetailInListResponse(
            id=like.id, created_at=like.created_at
        )
