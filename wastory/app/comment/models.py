from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.article.models import Article
    from wastory.app.user.models import User

class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(String(500), nullable=False)  # 500자로 확장 가능
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    secret: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped[Optional["User"]] = relationship("User", back_populates="comments")

    article_id: Mapped[int] = mapped_column(ForeignKey("article.id"), nullable=False)
    article: Mapped["Article"] = relationship("Article", back_populates="comments")

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comment.id"), nullable=True)
    children: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())    