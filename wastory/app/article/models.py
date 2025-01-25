from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.category.models import Category
    from wastory.app.blog.models import Blog
    from wastory.app.comment.models import Comment
    from wastory.app.like.models import Like
    from wastory.app.hometopic.models import Hometopic


class Article(Base):
    __tablename__ = "Article"

    id : Mapped[intpk]
    title : Mapped[str] = mapped_column(String(20), index=True, nullable = False)
    content : Mapped[str] = mapped_column(Text, nullable = False)
    description: Mapped[str] = mapped_column(String(100), nullable = False) # 미리보기용 description

    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False) # 조회수

    main_image_url: Mapped[str | None] = mapped_column(String(255), default=None, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())    
    # ondelete = "CASCADE" 를 통해 Article 삭제 시, Article 과 연결된 레코드에서 자동으로 참조가 제거.
    # blog 와 category 의 models 에서
    ## posts: Mapped[list["Article"]] = relationship("Article", back_populates="blog", cascade="all, delete-orphan")
    ## 식으로 정의해주면, blog 또는 category 삭제시 하위 항목도 같이 삭제됨.
    blog_id : Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete = "CASCADE"))
    category_id : Mapped[int] = mapped_column(ForeignKey("category.id", ondelete = "CASCADE"))
    hometopic_id : Mapped[int] = mapped_column(ForeignKey("hometopic.id", ondelete = "CASCADE"),nullable =True)  # 외래 키 정의

    """
    images : Mapped[list["Image"]] = relationship("Image", back_populates = "article", cascade = "all, delete-orphan")    
    """
    blog : Mapped["Blog"] = relationship("Blog", back_populates = "articles")
    category : Mapped["Category"] = relationship("Category", back_populates = "articles")
    
    # 이후 댓글 및 tag 구현시 delete-orphan 추가하기
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="article",  # Comment 모델의 article 관계명
        cascade="all, delete-orphan"  # Article 삭제 시 관련된 Comment도 삭제
    )
    likes : Mapped[list["Like"]] = relationship("Like", back_populates = "article", cascade = "all, delete-orphan")
    hometopic : Mapped["Hometopic"] = relationship("Hometopic", back_populates = "articles")
