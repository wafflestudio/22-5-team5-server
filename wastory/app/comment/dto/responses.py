from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from wastory.app.comment.models import Comment

class CommentDetailResponse(BaseModel):
    id : int
    user_name: str
    content : str
    created_at: datetime
    updated_at: datetime
    secret: int

    @staticmethod
    def from_comment(comment: Comment) -> "CommentDetailResponse":
        return CommentDetailResponse(
            id=comment.id,
            user_name=comment.user.nickname,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.created_at,
            secret=comment.secret
        )




