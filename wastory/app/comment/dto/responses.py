from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from wastory.app.comment.models import Comment


class CommentDetailResponse(BaseModel):
    id: int
    user_name: str
    content: str
    created_at: datetime
    updated_at: datetime
    secret: int

    @staticmethod
    def from_comment(comment: Comment) -> "CommentDetailResponse":
        return CommentDetailResponse(
            id=comment.id,
            user_name=comment.user_name,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            secret=comment.secret,
        )


class CommentListResponse(BaseModel):
    id: int
    user_name: str
    content: str
    created_at: datetime
    updated_at: datetime
    secret: int
    children: List[CommentDetailResponse]= []

    #이게 왜 있어야 하는지 모르겠어요
    class Config:
            orm_mode = True

    @staticmethod
    def from_comment(comment: Comment) -> "CommentListResponse":
        return CommentListResponse(
            id=comment.id,
            user_name=comment.user_name,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            secret=comment.secret,
            # children 리스트를 재귀적으로 변환
            children=[CommentDetailResponse.from_comment(child) for child in comment.children],
        )

class PaginatedCommentListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    comments: List[CommentListResponse]