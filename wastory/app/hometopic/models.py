from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, UniqueConstraint, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.article.models import Article


class Hometopic(Base):
    __tablename__ = "hometopic"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), index=True)
    high_category: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    articles: Mapped[list["Article"]] = relationship(
        "Article",
        back_populates="hometopic",  # Article의 hometopic과 연결
    )