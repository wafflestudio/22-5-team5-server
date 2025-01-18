from pydantic import BaseModel
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from wastory.app.comment.models import Comment

if TYPE_CHECKING:
    from wastory.app.user.models import User
    
class CommentDetailResponse(BaseModel):
    id: int
    user_name: str
    content: str
    created_at: datetime
    updated_at: datetime
    secret: int

    @staticmethod
    def from_comment(comment: Comment, current_user: Optional["User"]) -> "CommentDetailResponse":
        content_to_show = comment.content

        if comment.secret == 1:
            if not current_user:
                content_to_show = "비밀 댓글입니다"
            else:
                is_author = (comment.user_id == current_user.id)
                is_blog_owner = False
                if comment.blog and comment.blog.user_id == current_user.id:
                    is_blog_owner = True

                if not (is_author or is_blog_owner):
                    content_to_show = "비밀 댓글입니다"

        return CommentDetailResponse(
            id=comment.id,
            user_name=comment.user_name,
            content=content_to_show,
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
    children: List["CommentDetailResponse"] = []

    class Config:
        orm_mode = True

    @staticmethod
    def from_comment(comment: Comment, current_user: Optional["User"]) -> "CommentListResponse":
        # 기본적으로 댓글 내용을 보여주되,
        # secret이 1이면 권한을 확인해서 없으면 "비밀 댓글입니다"
        content_to_show = comment.content

        if comment.secret == 1:
            # 비밀 댓글일 때, 권한 판별
            if not current_user:
                # 비로그인 상태 -> 무조건 비밀 처리
                content_to_show = "비밀 댓글입니다"
            else:
                is_author = (comment.user_id == current_user.id)
                # 블로그 주인 판별 (blog.user_id가 current_user.id인지)
                is_blog_owner = False
                if comment.blog and comment.blog.user_id == current_user.id:
                    is_blog_owner = True

                if not (is_author or is_blog_owner):
                    # 작성자도 아니고 블로그 주인도 아니라면
                    content_to_show = "비밀 댓글입니다"

        # children도 같은 로직을 적용해야 하므로 재귀적으로 넘겨줌
        children_responses = [
            CommentDetailResponse.from_comment(child, current_user)
            for child in comment.children
        ]

        return CommentListResponse(
            id=comment.id,
            user_name=comment.user_name,
            content=content_to_show,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            secret=comment.secret,
            children=children_responses,
        )

class PaginatedCommentListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    comments: List[CommentListResponse]