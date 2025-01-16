from typing import Annotated

from fastapi import Depends
from wastory.app.article.dto.responses import ArticleDetailResponse, ArticleDetailInListResponse, ArticleSearchInListResponse
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.article.store import ArticleStore
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.blog.store import BlogStore
from wastory.app.category.errors import CategoryNotFoundError
from wastory.app.category.store import CategoryStore
from wastory.app.user.errors import PermissionDeniedError
from wastory.app.user.models import User

class ArticleService:
    def __init__(
        self,
        article_store: Annotated[ArticleStore, Depends()],
        blog_store: Annotated[BlogStore, Depends()],
        category_store: Annotated[CategoryStore, Depends()],
    ):
        self.article_store = article_store
        self.blog_store = blog_store
        self.category_store = category_store
    
    async def create_article(
        self, user: User, blog_id: int, category_id :int, article_title: str, article_content: str
    ) -> ArticleDetailResponse :
                
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        new_article = await self.article_store.create_article(blog_id, category_id, article_title, article_content)
        return ArticleDetailResponse.from_article(new_article)
    
    async def update_article(
        self, 
        user: User,
        article_id: int,
        article_title: str,
        article_content: str,
    ) -> ArticleDetailResponse:
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()

       
        
        # Article 존재 확인
        article = await self.article_store.get_article_by_id(article_id)
        if article is None: 
            raise ArticleNotFoundError()
        
        # 권한 검증
        if article.blog_id != user_blog.id:
            raise PermissionDeniedError()
    
        
        updated_article = await self.article_store.update_article(article, article_title, article_content)

        return ArticleDetailResponse.from_article(updated_article)
       
        
    async def get_articles_in_blog(
        self,
        blog_id: int,
    ) -> list[ArticleSearchInListResponse]:
        articles = await self.article_store.get_articles_in_blog(blog_id)
        return [ArticleSearchInListResponse.from_article(article) for article in articles]
    
    async def get_articles_in_blog_in_category(
        self,
        category_id: int,
        blog_id: int,
    ) -> list[ArticleSearchInListResponse]:
        articles = await self.article_store.get_articles_in_blog_in_category(category_id, blog_id)
        return [ArticleSearchInListResponse.from_article(article) for article in articles]    

    async def get_articles_by_words_and_blog_id(
        self,
        searching_words: str | None = None,
        blog_id: int | None = None
    ) -> list[ArticleSearchInListResponse]:
        articles = await self.article_store.get_articles_by_words_and_blog_id(searching_words, blog_id)
        return [ArticleSearchInListResponse.from_article(article) for article in articles]

    
    async def delete_article(
        self,
        user: User,
        article_id: int,
    ) -> None:

        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)  # await 추가
        if user_blog is None:
            raise BlogNotFoundError()


        # Article 존재 확인
        article = await self.article_store.get_article_by_id(article_id)  # await 추가
        if article is None:
            raise ArticleNotFoundError()

        # 권한 검증
        if article.blog_id != user_blog.id:
            raise PermissionDeniedError()
    

        # Article 삭제
        await self.article_store.delete_article(article)  # await 추가