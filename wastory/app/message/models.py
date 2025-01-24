from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.user.models import User

class Message(Base):
    __tablename__ = "message"

    id: Mapped[intpk]
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")

    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")

