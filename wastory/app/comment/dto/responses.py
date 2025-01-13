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
            
        )




