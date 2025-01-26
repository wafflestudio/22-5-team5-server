from typing import Annotated

from fastapi import Depends
from wastory.app.article.dto.responses import ArticleDetailResponse, PaginatedArticleListResponse, ArticleInformationResponse,DraftListResponse,DraftResponse
from wastory.app.article.errors import ArticleNotFoundError,ArticleNotDraftError,ArticleNotPublishedError
from wastory.app.article.store import ArticleStore
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.blog.store import BlogStore
from wastory.app.hometopic.store import HometopicStore
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
        self, user: User, category_id :int, hometopic_id : int, article_title: str, article_content: str, article_description: str,
    ) -> ArticleDetailResponse :
                
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
            
        new_article = await self.article_store.create_article(
            blog_id=user_blog.id, 
            category_id=category_id, 
            article_title=article_title, 
            article_content=article_content, 
            article_description = article_description,
            hometopic_id = hometopic_id
            )

        # 새 글 알림
        await self.notification_service.add_notification(
            blog_address_names = await self.subscription_store.get_subscriber_blog_addresses(user_blog.id),
            type = 1,
            username = user.username,
            notification_blogname= user_blog.blog_name,
            description = article_title,
        )

        return ArticleDetailResponse.from_article(new_article)

    async def publish_draft(
        self, user: User, category_id :int, hometopic_id : int, article_title: str, article_content: str, article_description: str,article_id:int
    ) -> ArticleDetailResponse :
                
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        
        new_article = await self.article_store.publish_draft(
            blog_id=user_blog.id, 
            category_id=category_id, 
            article_title=article_title, 
            article_content=article_content, 
            article_description = article_description,
            hometopic_id = hometopic_id,
            article_id=article_id
            )

        # 새 글 알림
        await self.notification_service.add_notification(
            blog_address_names = await self.subscription_store.get_subscriber_blog_addresses(user_blog.id),
            type = 1,
            username = user.username,
            notification_blogname= user_blog.blog_name,
            description = article_title,
        )

        return ArticleDetailResponse.from_article(new_article)

    async def create_draft(
        self, user: User, category_id :int, hometopic_id : int, article_title: str, article_content: str, article_description: str,
    )->ArticleDetailResponse:
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
            
        new_article = await self.article_store.create_draft(
            blog_id=user_blog.id, 
            category_id=category_id, 
            atricle_title=article_title, 
            article_content=article_content, 
            article_description = article_description,
            hometopic_id = hometopic_id
            )
        return DraftResponse.from_draft(new_article)

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

    async def update_draft(
        self, 
        user: User,
        article_id: int,
        article_title: str,
        article_content: str,
    ) -> DraftResponse:
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()


        # Article 존재 확인
        draft = await self.article_store.get_draft_by_id(article_id)
        if draft is None: 
            raise ArticleNotFoundError()
        
        # 권한 검증
        if draft.blog_id != user_blog.id:
            raise PermissionDeniedError()
    
        
        updated_draft = await self.article_store.update_draft(draft, article_title, article_content)

        return DraftResponse.from_draft(updated_draft)
    
    async def get_article_information_by_id(self, article_id : int) -> ArticleInformationResponse:
        # 조회수 증가
        article = self.article_store.get_article_information_by_id(article_id)
        await self.article_store.increment_article_views(article_id)
        return await article
    
    async def get_draft_information_by_id(self, user:User,article_id : int) -> DraftResponse:
        article = await self.article_store.get_draft_by_id(article_id)
        if article.blog_id!=user.blogs.id:
            raise PermissionDeniedError
        if article.draft==False:
            raise ArticleNotDraftError
        return DraftResponse.from_draft(article)
    
    async def get_today_most_viewed(
        self,
        page : int
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_today_most_viewed(page)

    async def get_weekly_most_viewed(
        self,
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_weekly_most_viewed()
        
    async def get_most_viewed_in_hometopic(
        self,
        high_hometopic_id: int,
        page: int,
    ) -> PaginatedArticleListResponse:
        hometopic_id_list = await self.hometopic_store.get_hometopic_id_list_by_high_hometopic_id(high_hometopic_id)
        return await self.article_store.get_most_viewed_in_hometopic(
            hometopic_id_list=hometopic_id_list, 
            page=page
        )   
        
    async def get_articles_in_blog(
        self,
        blog_id: int,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_in_blog(blog_id=blog_id, page=page, per_page=per_page)

    async def get_drafts_in_blog(
        self,
        user: User,
        page: int,
        per_page: int
    ) -> DraftListResponse:
        return await self.article_store.get_drafts_in_blog(blog_id=user.blogs.id, page=page, per_page=per_page)
    
    async def get_articles_in_blog_in_category(
        self,
        blog_id: int,
        category_id: int,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_in_blog_in_category(
            category_id=category_id, blog_id=blog_id, page=page, per_page=per_page
        )
    async def get_articles_by_words_and_blog_id(
        self,
        searching_words: str | None,
        blog_id: int | None,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_articles_by_words_and_blog_id(
            searching_words=searching_words, blog_id=blog_id, page=page, per_page=per_page
        )
    
    async def get_articles_of_subscriptions(
        self,
        user : User,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse : 
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        return await self.article_store.get_articles_of_subscriptions(
            blog_id = user_blog.id, page = page, per_page = per_page
        )
    
    async def get_top_articles_in_blog(
        self,
        blog_id: int,
        sort_by: str,
    ) -> PaginatedArticleListResponse:
        return await self.article_store.get_top_articles_in_blog(
            blog_id=blog_id, sort_by=sort_by)

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

    async def delete_draft(
        self,
        user: User,
        article_id: int,
    ) -> None:

        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)  # await 추가
        if user_blog is None:
            raise BlogNotFoundError()


        # Article 존재 확인
        article = await self.article_store.get_draft_by_id(article_id)  # await 추가
        if article is None:
            raise ArticleNotFoundError()

        # 권한 검증
        if article.blog_id != user_blog.id:
            raise PermissionDeniedError()
    

        # Article 삭제
        await self.article_store.delete_article(article)  # await 추가

    