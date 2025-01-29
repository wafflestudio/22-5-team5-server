from typing import Annotated

from fastapi import Depends
from wastory.app.article.dto.responses import ArticleDetailResponse, PaginatedArticleListResponse, ArticleInformationResponse
from wastory.app.article.errors import ArticleNotFoundError, NoAuthoriztionError
from wastory.app.article.store import ArticleStore
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.blog.store import BlogStore
from wastory.app.hometopic.store import HometopicStore
from wastory.app.hometopic.errors import InvalidhometopicError
from wastory.app.category.store import CategoryStore
from wastory.app.subscription.store import SubscriptionStore
from wastory.app.notification.service import NotificationService
from wastory.app.user.errors import PermissionDeniedError
from wastory.app.user.models import User 

class ArticleService:
    def __init__(
        self,
        article_store: Annotated[ArticleStore, Depends()],
        blog_store: Annotated[BlogStore, Depends()],
        category_store: Annotated[CategoryStore, Depends()],
        subscription_store: Annotated[SubscriptionStore, Depends()],
        hometopic_store : Annotated[HometopicStore, Depends()],
        notification_service: Annotated[NotificationService, Depends()],
    ):
        self.article_store = article_store
        self.blog_store = blog_store
        self.category_store = category_store
        self.subscription_store = subscription_store
        self.notification_service = notification_service
        self.hometopic_store = hometopic_store
    
    async def create_article(
        self, 
        user: User, 
        article_title: str, 
        article_content: str, 
        article_description: str,
        main_image_url : str | None,
        category_id :int, 
        hometopic_id : int, 
        secret : int = 0
    ) -> ArticleDetailResponse :
                
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        # 유효한 hometopic_id 범위 검사
        if hometopic_id <= 0 or (2 <= hometopic_id <= 9) or hometopic_id >= 54:
            raise InvalidhometopicError    
        
        new_article = await self.article_store.create_article(
            atricle_title=article_title, 
            article_content=article_content, 
            article_description = article_description,
            main_image_url = main_image_url,
            blog_id=user_blog.id, 
            category_id=category_id, 
            hometopic_id = hometopic_id,
            secret=secret
        )

        # 새 글 알림
        await self.notification_service.add_notification(
            blog_address_names = await self.subscription_store.get_subscriber_blog_addresses(user_blog.id),
            type = 1,
            notification_blog_name = user_blog.blog_name,
            notification_blog_image_url = user_blog.main_image_url,
            article_id=new_article.id
        )

        return ArticleDetailResponse.from_article(new_article)
    
    async def update_article(
        self, 
        user: User,
        article_id: int,
        article_title: str,
        article_content: str,
        article_description : str,
        main_image_url : str | None,
        category_id : int,
        hometopic_id : int,
        secret : int | None
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
        
        # 유효한 hometopic_id 범위 검사
        if hometopic_id <= 0 or (2 <= hometopic_id <= 9) or hometopic_id >= 54:
            raise InvalidhometopicError 
    
        
        updated_article = await self.article_store.update_article(
            article, 
            article_title, 
            article_content,
            article_description,
            main_image_url,
            category_id,
            hometopic_id,
            secret
        )

        return ArticleDetailResponse.from_article(updated_article)

    async def get_article_information_by_id(self, user: User, article_id: int) -> ArticleInformationResponse:
        article = await self.article_store.get_article_by_id(article_id)
        
        # Article 존재 확인
        if article is None:
            raise ArticleNotFoundError()

        # 비밀글 접근 권한 확인
        if article.secret == 1 and article.blog.user_id != user.id:
            raise NoAuthoriztionError()

        # 조회수 증가
        await self.article_store.increment_article_views(article_id)
        return await self.article_store.get_article_information_by_id(article_id)
    
    async def get_today_most_viewed(
        self,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_today_most_viewed(user=user)

    async def get_weekly_most_viewed(
        self,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_weekly_most_viewed(user=user)
        
    async def get_most_viewed_in_hometopic(
        self,
        user : User,
        high_hometopic_id: int,
        page: int,
    ) -> PaginatedArticleListResponse:

        # 유효한 hometopic_id    검사
        if high_hometopic_id <= 1 or high_hometopic_id >= 10:
            raise InvalidhometopicError
        
        hometopic_id_list = await self.hometopic_store.get_hometopic_id_list_by_high_hometopic_id(high_hometopic_id)
        return await self.article_store.get_most_viewed_in_hometopic(
            user=user,
            hometopic_id_list=hometopic_id_list, 
            page=page,
            per_page = 7
        )

    async def get_focus_view_of_article_Js_weekend_plan(
        self,
        user : User
    ) -> PaginatedArticleListResponse:

        hometopic_id_list = [10,11,12,13]
        return await self.article_store.get_most_viewed_in_hometopic(
            hometopic_id_list=hometopic_id_list, 
            user = user,
            page = 1,
            per_page = 5
        )
    async def get_focus_view_of_article_coffee(
        self,
        user : User
    ) -> PaginatedArticleListResponse:

        hometopic_id_list = [14]
        return await self.article_store.get_most_viewed_in_hometopic(
            hometopic_id_list=hometopic_id_list, 
            user=user,
            page = 1,
            per_page = 5
        )            
        
    async def get_articles_in_blog(
        self,
        user: User,
        blog_id: int,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_in_blog(blog_id=blog_id, page=page, per_page=per_page, user=user)
    
    async def get_articles_in_blog_in_category(
        self,
        blog_id: int,
        category_id: int,
        page: int,
        per_page: int,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_in_blog_in_category(
            category_id=category_id, blog_id=blog_id, page=page, per_page=per_page, user=user
        )
    async def get_articles_by_words_and_blog_id(
        self,
        searching_words: str | None,
        blog_id: int | None,
        page: int,
        per_page: int,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_by_words_and_blog_id(
            searching_words=searching_words, blog_id=blog_id, page=page, per_page=per_page, user=user
        )
    
    async def get_articles_of_subscriptions(
        self,
        user : User,
        page: int,
        per_page: int,
    ) -> PaginatedArticleListResponse : 
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        return await self.article_store.get_articles_of_subscriptions(
            user = user, user_blog=user_blog, page = page, per_page = per_page
        )
    
    async def get_top_articles_in_blog(
        self,
        blog_id: int,
        sort_by: str,
        user : User
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_top_articles_in_blog(
            blog_id=blog_id, sort_by=sort_by, user=user)

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

    