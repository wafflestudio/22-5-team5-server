from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Boolean, ForeignKey, CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.user.models import User
    from wastory.app.blog.models import Blog
    from wastory.app.category.models import Category
    from wastory.app.article.models import Article
    from wastory.app.comment.models import Comment

class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = (
        CheckConstraint("notification_type IN (1, 2, 3, 4, 5)", name="valid_notification_type"), # type은 5개 카테고리만 허용
    )

    id: Mapped[intpk]
    notification_blogname: Mapped[str | None] = mapped_column(String(20)) # 알림에 사용되는 블로그 이름
    username: Mapped[str | None] = mapped_column(String(20)) # 알림 생성자 유저 이름
    notification_type: Mapped[int] = mapped_column(Integer, nullable=False) # 새 글 알림(1), 구독 알림(2), 댓글 알림(3), 방명록 알림(4), 쪽지 알림(5)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())  # 생성 시간
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())  # 갱신 시간
    checked: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="0")  # 확인 여부 (기본값 False)
    notification_blog_image_url: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)


    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # 알림 소유자
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete="CASCADE"), nullable=False)  # 알림 소유자
    article_id: Mapped[int] = mapped_column(ForeignKey("Article.id", ondelete="CASCADE"), nullable=True)  # 관련 글
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id", ondelete="CASCADE"), nullable=True)  # 관련 댓글


    # 관계 설정
    user: Mapped["User"] = relationship("User", back_populates="notification")
    blog: Mapped["Blog"] = relationship("Blog", back_populates="notification")
    article: Mapped["Article"] = relationship("Article", back_populates="notification")
    comments: Mapped["Comment"] = relationship("Comment", back_populates="notification")