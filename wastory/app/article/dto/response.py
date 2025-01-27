from pydantic import BaseModel
from datetime import datetime

class ArticleBaseResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    views: int

    class Config:
        from_attributes = True


class ArticleBlogInfoMixin(BaseModel):
    blog_id: int
    blog_name: str
    blog_main_image_url: str | None


class ArticleInteractionMixin(BaseModel):
    article_likes: int
    article_comments: int


class ArticleInformationResponse(ArticleBaseResponse, ArticleBlogInfoMixin, ArticleInteractionMixin):
    content: str
    category_id: int

    @staticmethod
    def from_article(
        article: "Article" | None,
        blog_name: str,
        blog_main_image_url: str | None,
        article_likes: int,
        article_comments: int,
    ) -> "ArticleInformationResponse":
        if article is None:
            raise ArticleNotFoundError

        return ArticleInformationResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            created_at=article.created_at,
            updated_at=article.updated_at,
            views=article.views,
            blog_id=article.blog_id,
            category_id=article.category_id,
            blog_name=blog_name,
            blog_main_image_url=blog_main_image_url,
            article_likes=article_likes,
            article_comments=article_comments,
        )


class ArticleDetailResponse(ArticleBaseResponse):
    content: str

    @staticmethod
    def from_article(article: "Article") -> "ArticleDetailResponse":
        return ArticleDetailResponse(
            id=article.id,
            title=article.title,
            content=article.content,
            created_at=article.created_at,
            updated_at=article.updated_at,
            views=article.views,
        )


class ArticleSearchInListResponse(ArticleBaseResponse, ArticleBlogInfoMixin, ArticleInteractionMixin):
    description: str

    @staticmethod
    def from_article(
        article: "Article" | None,
        blog_name: str,
        blog_main_image_url: str | None,
        article_likes: int,
        article_comments: int,
    ) -> "ArticleSearchInListResponse":
        if article is None:
            raise ArticleNotFoundError

        return ArticleSearchInListResponse(
            id=article.id,
            title=article.title,
            description=article.description,
            created_at=article.created_at,
            updated_at=article.updated_at,
            views=article.views,
            blog_id=article.blog_id,
            blog_name=blog_name,
            blog_main_image_url=blog_main_image_url,
            article_likes=article_likes,
            article_comments=article_comments,
        )


class PaginatedArticleListResponse(BaseModel):
    page: int
    per_page: int
    total_count: int
    articles: list[ArticleSearchInListResponse]
