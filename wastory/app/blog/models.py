from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.user.models import User
    from wastory.app.category.models import Category
    from wastory.app.article.models import Article
    from wastory.app.guestbook.models import GuestBook

class Blog(Base):
    __tablename__ = "blog"
    __table_args__ = (
        UniqueConstraint("user_id", name="unique_user_blog"),  # 각 유저당 하나의 블로그만 생성 가능
    )

    id: Mapped[intpk] # 블로그 아이디
    blog_name: Mapped[str] = mapped_column(String(100), nullable=False)  # 블로그 제목
    address_name: Mapped[str]=mapped_column(String(100), nullable=False) # 주소 이름
    description: Mapped[str | None] = mapped_column(String(255))  # 블로그 설명 (선택적)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())  # 생성 시간
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())  # 갱신 시간
    main_image_url: Mapped[str|None] = mapped_column(String(255), nullable=True, server_default=None)


    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)  # 블로그 소유자

    # 관계 설정
    user: Mapped["User"] = relationship("User", back_populates="blogs")
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="blog")
    articles: Mapped[list["Article"]] = relationship("Article",  back_populates="blog")


    def __repr__(self):
        return f"<Blog id={self.id}, blog_name={self.blog_name}, user_id={self.user_id}>"
