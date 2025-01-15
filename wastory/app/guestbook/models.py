from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.comment.models import Comment
    from wastory.app.blog.models import Blog
    
class GuestBook(Base):
    __tablename__ = "guestbook"

    id: Mapped[intpk]
    
    # 다른 필요한 컬럼들도 추가 가능
    # 예) 방명록의 작성자, 제목, 공개 여부 등
    blog_name: Mapped[str] = mapped_column(String(100), nullable=False)
    blog_id : Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete = "CASCADE"))
    blog : Mapped["Blog"] = relationship("Blog", back_populates = "articles")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        default=func.now(), 
        onupdate=func.now()
    )

    # GuestBook과 Comment를 연결
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="guestbook",       # Comment 모델의 guestbook 관계명
        cascade="all, delete-orphan"
    )