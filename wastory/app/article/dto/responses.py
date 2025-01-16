from typing import Self
from pydantic import BaseModel
from datetime import datetime
from wastory.app.article.models import Article


class ArticleDetailResponse(BaseModel):
    id : int
    title : str
    content : str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_article(article: Article) -> "ArticleDetailResponse":
        return ArticleDetailResponse(
            id=article.id, title=article.title, content=article.content, created_at=article.created_at, updated_at = article.updated_at
        )

class ArticleSearchResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
    @staticmethod
    def from_article(article: Article) -> "ArticleDetailResponse":
        return ArticleDetailResponse(
            id=article.id, title=article.title, content=article.content, created_at=article.created_at, updated_at = article.updated_at
        )
    
class ArticleSearchInListResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

    # 설정 추가
    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(article: Article) -> "ArticleSearchInListResponse":
        return ArticleSearchInListResponse(
            id=article.id, title=article.title, description=article.description, created_at=article.created_at, updated_at = article.updated_at
        )

