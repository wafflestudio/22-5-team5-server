from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, UniqueConstraint, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.user.models import User
    from wastory.app.blog.models import Blog


class Category(Base):
    __tablename__ = "category"
    __table_args__ = (
        UniqueConstraint("name", "blog_id", name="unique_category_per_blog"),  # 동일 블로그 내에서 이름 중복 방지
        CheckConstraint("level IN (1, 2)", name="valid_category_level"),       # level은 1(상위) 또는 2(하위)만 허용
    )

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), index=True)
    blog: Mapped["Blog"]=relationship("Blog", back_populates="categories")
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog.id"))
    level: Mapped[int] = mapped_column(Integer, nullable=False)  
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"), nullable=True)

    # 양방향 관계 설정
    parent: Mapped["Category"] = relationship(
        "Category",
        back_populates="children",
        remote_side="Category.id"  # 충돌 방지를 위해 명시
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan"
    )


    