from sqlalchemy import ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wastory.app.blog.models import Blog

class Subscription(Base):
    __tablename__ = "blog_subscription"

    __table_args__ = (
        UniqueConstraint("subscriber_id", "subscribed_id", name="unique_subscription"),
    )

    id: Mapped[intpk]  # 구독 관계의 고유 ID
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete="CASCADE"), nullable=True)  # 구독자
    subscribed_id: Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete="CASCADE"), nullable=True)  # 피구독자
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())  # 생성 시간

    # 관계 설정
    subscriber: Mapped["Blog"] = relationship("Blog", foreign_keys=[subscriber_id], back_populates="subscriptions")
    subscribed_blog: Mapped["Blog"] = relationship("Blog", foreign_keys=[subscribed_id], back_populates="subscribers")