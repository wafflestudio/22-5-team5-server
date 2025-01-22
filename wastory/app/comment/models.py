from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, Integer, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.article.models import Article
    from wastory.app.user.models import User
    from wastory.app.blog.models import Blog  

class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    secret: Mapped[int] = mapped_column(Integer, nullable=False, default=False)
    user_name:Mapped[str]=mapped_column(String(20), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped[Optional["User"]] = relationship("User", back_populates="comments")

    # Article에 대한 FK
    article_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Article.id", ondelete="CASCADE"), nullable=True, index=True)
    article: Mapped[Optional["Article"]] = relationship("Article", back_populates="comments")

    blog_id: Mapped[Optional[int]] = mapped_column(ForeignKey("blog.id", ondelete="CASCADE"), nullable=True, index=True)
    blog: Mapped[Optional["Blog"]] = relationship("Blog", back_populates="comments")

    # 자기 자신의 FK(부모 댓글)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comment.id"), nullable=True)
    parent: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        back_populates="children",
        remote_side="Comment.id"
    )

    # 자식 댓글
    children: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "(article_id IS NOT NULL OR blog_id IS NOT NULL)",
            name="check_article_or_blog"
        ),
    )