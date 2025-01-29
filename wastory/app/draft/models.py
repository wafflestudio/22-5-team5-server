from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.blog.models import Blog


class Draft(Base):
    __tablename__ = "draft"

    id : Mapped[intpk]
    title : Mapped[str] = mapped_column(String(80), index=True, nullable = False)
    content : Mapped[str] = mapped_column(Text, nullable = False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    blog_id : Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete = "CASCADE"))
    blog : Mapped["Blog"] = relationship("Blog", back_populates = "drafts")
