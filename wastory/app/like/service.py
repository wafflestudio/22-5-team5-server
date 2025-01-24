from typing import Annotated

from fastapi import Depends
from wastory.app.like.dto.responses import LikeDetailResponse, LikeDetailInListResponse
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.article.store import ArticleStore
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.blog.store import BlogStore
from wastory.app.user.errors import PermissionDeniedError
from wastory.app.user.models import User
from wastory.app.like.store import LikeStore
from wastory.app.like.errors import LikeNotFoundError, LikeAlreadyExistsError

class LikeService:
    def __init__(
        self,
        like_store: Annotated[LikeStore, Depends()],
        blog_store: Annotated[BlogStore, Depends()],
        article_store: Annotated[ArticleStore, Depends()],
    ):
        self.like_store = like_store
        self.blog_store = blog_store
        self.article_store = article_store
    
    async def create_like(
        self, user: User, blog_id: int, article_id :int,
    ) -> LikeDetailResponse :
                
        # like 를 누르는 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        # article 존재 검증
        article = await self.article_store.get_article_by_id(article_id)
        if article is None:
            raise ArticleNotFoundError()

        # 좋아요가 이미 존재하는지 검증
        existing_like = await self.like_store.get_like_by_blog_and_article(blog_id, article_id)
        if existing_like is not None:
            raise LikeAlreadyExistsError()

        new_like = await self.like_store.create_like(blog_id, article_id)
        return LikeDetailResponse.from_like(new_like)
    
    async def delete_like_in_article(
        self,
        user: User,
        article_id: int
    ) -> None:

        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()


        # like 존재 확인
        like = await self.like_store.get_like_by_blog_in_article(
            blog_id = user_blog.id,
            article_id = article_id
        ) 
        if like is None:
            raise LikeNotFoundError()    

        # Article 삭제
        await self.like_store.delete_like(like) 
       
        
    async def get_likes_by_blog(
        self,
        blog_id: int,
    ) -> list[LikeDetailInListResponse]:
        likes = await self.like_store.get_likes_by_blog(blog_id)
        return [LikeDetailInListResponse.from_like(like) for like in likes]
    
    async def get_likes_in_article(
        self,
        article_id: int,
    ) -> list[LikeDetailInListResponse]:
        likes = await self.like_store.get_likes_in_article(article_id)
        return [LikeDetailInListResponse.from_like(article) for article in likes]    

    async def blog_press_like(
        self,
        blog_id: int,
        article_id: int,
    ) -> bool:
        return await self.like_store.blog_press_like(blog_id, article_id)

    