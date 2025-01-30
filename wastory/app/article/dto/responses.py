from fastapi import Depends
from typing import Self, Annotated, Optional
from pydantic import BaseModel
from datetime import datetime
from wastory.app.article.models import Article
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.blog.store import BlogStore


class ArticleInformationResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    article_main_image_url: Optional[str] = None
    protected: int

    blog_id: int
    blog_name: str
    blog_main_image_url: Optional[str] = None
    category_id: int

    views: int

    article_likes: int
    article_comments: int

    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(
        article: Optional[Article], 
        blog_name: str, 
        blog_main_image_url: Optional[str], 
        article_likes: int, 
        article_comments: int
    ) -> Self:
        if article is None:
            raise ArticleNotFoundError

        return ArticleInformationResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            created_at=article.created_at,
            updated_at=article.updated_at,
            article_main_image_url=article.main_image_url,
            views=article.views,
            blog_id=article.blog_id,
            category_id=article.category_id,
            blog_name=blog_name,
            blog_main_image_url=blog_main_image_url,
            article_likes=article_likes,
            article_comments=article_comments,
            protected=article.protected
        )


class ArticleDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    views: int
    protected: int

    @staticmethod
    def from_article(article: Article) -> Self:
        return ArticleDetailResponse(
            id=article.id,
            title=article.title,
            content=article.content if article.protected == 0 else "🔒 보호된 게시글입니다.",
            created_at=article.created_at,
            updated_at=article.updated_at,
            views=article.views,
            protected=article.protected
        )


class ArticleSearchInListResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    article_main_image_url: Optional[str] = None

    blog_id: int
    blog_name: str
    blog_main_image_url: Optional[str] = None

    views: int
    article_likes: int
    article_comments: int
    protected: int

    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(
        article: Optional[Article], 
        blog_name: str, 
        blog_main_image_url: Optional[str], 
        article_likes: int, 
        article_comments: int
    ) -> Self:
        if article is None:
            raise ArticleNotFoundError

        return ArticleSearchInListResponse(
            id=article.id,
            title=article.title,
            description=article.description if article.protected == 0 else "🔒 보호된 게시글입니다.",
            created_at=article.created_at,
            updated_at=article.updated_at,
            article_main_image_url=article.main_image_url,
            views=article.views,
            blog_id=article.blog_id,
            blog_name=blog_name,
            blog_main_image_url=blog_main_image_url,
            article_likes=article_likes,
            article_comments=article_comments,
            protected=article.protected
        )


class PaginatedArticleListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    articles: list[ArticleSearchInListResponse]
