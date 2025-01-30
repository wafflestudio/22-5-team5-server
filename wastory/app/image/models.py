from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.article.models import Article
    from wastory.app.blog.models import Blog

    


class Image(Base):
    __tablename__ = "image"

    id: Mapped[intpk]
    file_url: Mapped[str] = mapped_column(String(200), nullable=False)
    article_id: Mapped[int | None] = mapped_column(ForeignKey("Article.id", ondelete="CASCADE"), nullable=True)
    blog_id: Mapped[int | None] = mapped_column(ForeignKey("blog.id", ondelete="CASCADE"), nullable=True)
    is_main: Mapped[bool] = mapped_column(default=False)  # ✅ 대표 이미지 여부 추가

    article: Mapped["Article"] = relationship("Article", back_populates="images")
    blog: Mapped["Blog"] = relationship("Blog", back_populates="main_image")
    
    
 