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


class ArticleDetailInListResponse(BaseModel):
    id : int
    title : str
    content : str
    created_at: datetime
    updated_at: datetime


    @staticmethod
    def from_article(article: Article) -> "ArticleDetailInListResponse":
        return ArticleDetailInListResponse(
            id=article.id, title=article.title, content=article.content, created_at=article.created_at, updated_at = article.updated_at
        )
