from fastapi import Depends
from typing import Self, Annotated
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
    article_main_image_url : str | None

    blog_id: int
    blog_name : str
    blog_main_image_url : str | None
    article_main_image_url : str | None
    category_id : int 

    views: int

    article_likes: int
    article_comments : int

    # 설정 추가
    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(article: Article | None, blog_name : str, blog_main_image_url :str | None, article_likes: int, article_comments: int) -> "ArticleInformationResponse":
        if article is None : 
            raise ArticleNotFoundError

        return ArticleInformationResponse(
            id=article.id, 
            title=article.title, 
            content=article.content,
            created_at=article.created_at, 
            updated_at = article.updated_at,
            
            article_main_image_url = article.main_image_url,

            views = article.views,
            blog_id = article.blog_id,
            category_id = article.category_id,
            blog_name = blog_name,
            blog_main_image_url = blog_main_image_url,
            article_main_image_url = article.main_image_url,
            article_likes = article_likes,
            article_comments = article_comments
        )
    
class ArticleDetailResponse(BaseModel):
    id : int
    title : str
    content : str
    created_at: datetime
    updated_at: datetime

    views: int

    @staticmethod
    def from_article(article: Article) -> "ArticleDetailResponse":
        return ArticleDetailResponse(
            id=article.id, title=article.title, content=article.content, created_at=article.created_at, updated_at = article.updated_at, views = article.views
        )


    
class ArticleSearchInListResponse(BaseModel):

    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    article_main_image_url : str | None


    blog_id: int
    blog_name : str
    blog_main_image_url : str | None
    article_main_image_url : str | None

    views: int

    article_likes: int
    article_comments : int

    # 설정 추가
    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_article(article: Article | None, blog_name : str, blog_main_image_url :str | None, article_likes: int, article_comments: int) -> "ArticleSearchInListResponse":
        
        
        return ArticleSearchInListResponse(
            id=article.id, 
            title=article.title, 
            description=article.description, 
            created_at=article.created_at, 
            updated_at = article.updated_at,
            article_main_image_url = article.main_image_url,

            views = article.views,
            blog_id = article.blog_id,
            blog_name = blog_name,
            blog_main_image_url = blog_main_image_url,
            article_main_image_url = article.main_image_url,
            article_likes = article_likes,
            article_comments = article_comments
        )

class PaginatedArticleListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    articles: list[ArticleSearchInListResponse]