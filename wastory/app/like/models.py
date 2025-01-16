from typing import TYPE_CHECKING
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wastory.database.common import Base, intpk

if TYPE_CHECKING:
    from wastory.app.blog.models import Blog
    from wastory.app.article.models import Article
class Like(Base):
    #tablename like 이 mysql 상에서 사용되어서 blog_like 로 하였음.
    __tablename__ = "blog_like"

    id : Mapped[intpk]
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
   
 
    # blog_id who gives like to article
    # user_id 보다는 blog 측면에서 작동하는게 나을 것 같아서 blog 로 했습니다.
    blog_id : Mapped[int] = mapped_column(ForeignKey("blog.id", ondelete = "CASCADE"), nullable = False)
    # article_id which get like from blog
    article_id : Mapped[int] = mapped_column(ForeignKey("Article.id", ondelete = "CASCADE"), nullable = False)
    
    #
    article : Mapped["Article"] = relationship("Article", back_populates = "likes")
    blog : Mapped["Blog"] = relationship("Blog", back_populates = "likes")
    # 이후 구현 시 delete-orphan 추가하기
    # ondelete = "CASCADE" 를 통해 like 삭제 시, like 과 연결된 레코드에서 자동으로 참조가 제거.
    # blog 와 article 의 models 에서
    ## posts: Mapped[list["Article"]] = relationship("Article", back_populates="blog", cascade="all, delete-orphan")
    ## 식으로 정의해주면, blog 또는 category 삭제시 하위 항목도 같이 삭제됨.