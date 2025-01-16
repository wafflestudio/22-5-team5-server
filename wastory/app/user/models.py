from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.blog.models import Blog
    from wastory.app.notification.models import Notification

class User(Base):
    __tablename__ = "user"
    

    id: Mapped[intpk]
    username: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    nickname: Mapped[str | None] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(20))


    blogs = relationship("Blog", lazy="selectin", back_populates="user", uselist=False)
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",  # Comment 모델의 article 관계명
        cascade="all, delete-orphan"  # Article 삭제 시 관련된 Comment도 삭제
    )
    notification = relationship("Notification", lazy="selectin", back_populates="user", uselist=False)
    
class BlockedToken(Base):
    __tablename__ = "blocked_token"

    token_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime)