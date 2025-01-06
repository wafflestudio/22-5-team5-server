from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.blog.models import Blog

class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(20))

    # Blog와의 관계 (각 유저당 하나의 블로그)
    blogs: Mapped["Blog"] = relationship("Blog", back_populates="user", uselist=False)
