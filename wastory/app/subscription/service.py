from typing import Annotated, List
from fastapi import Depends
from wastory.app.subscription.store import SubscriptionStore
from wastory.app.subscription.dto.responses import SubscriptionDetailResponse, PaginatedSubscriptionResponse
from wastory.app.user.service import UserService
from wastory.app.blog.service import BlogService
from wastory.app.notification.service import NotificationService
from wastory.app.subscription.errors import BlogNotFoundError, SelfSubscriptionError
from wastory.app.user.models import User
from wastory.app.blog.dto.responses import BlogDetailResponse


class SubscriptionService:
    def __init__(
            self,
            subscription_store: Annotated[SubscriptionStore, Depends()],
            user_service: Annotated[UserService, Depends()],
            blog_service: Annotated[BlogService, Depends()],
            notification_service: Annotated[NotificationService, Depends()],
            ) -> None:
        self.subscription_store = subscription_store
        self.user_service=user_service
        self.blog_service=blog_service
        self.notification_service = notification_service

    async def add_subscription(self, subscriber_id: int, subscribed_id: int) -> SubscriptionDetailResponse:
        """
        구독 추가 서비스
        """
        subscribed_blog = await self.blog_service.get_blog_by_id(subscribed_id)
        subscriber_blog = await self.blog_service.get_blog_by_id(subscriber_id)
        subscriber = await self.user_service.get_user_by_id(subscriber_blog.user_id)

        # SubscriptionStore에서 구독 추가 호출
        subscription = await self.subscription_store.add_subscription(subscriber_id, subscribed_id)

        # 구독 알림
        await self.notification_service.add_notification(
            blog_address_names = [subscribed_blog.address_name],
            type=2,
            username=subscriber.username,
            notification_blogname=subscriber_blog.blog_name,
            description="구독",
        )

        # SubscriptionDetailResponse로 변환하여 반환
        return SubscriptionDetailResponse.model_validate(subscription, from_attributes=True)
    
    async def cancel_subscription(self, subscriber_user: User, subscribed_address_name: str) -> bool:
        """
        구독 취소 서비스
        """
        # 구독 대상 블로그 정보 가져오기
        subscribed_blog = await self.blog_service.get_blog_by_address_name(subscribed_address_name)
        subscriber_blog = await self.blog_service.get_blog_by_user(user=subscriber_user)
        if not subscribed_blog or not subscriber_blog:
            raise BlogNotFoundError # 취소할 블로그가 없는 경우

        # 구독 관계 삭제
        return await self.subscription_store.delete_subscription(subscriber_blog.id, subscribed_blog.id)
    
    async def get_paginated_subscribed_blog_address(self, subscriber: User, page: int, per_page: int)->PaginatedSubscriptionResponse:
        """
        내가 구독 중인 블로그들의 정보 반환(페이지네이션)
        """
        subscriber_blog=await self.blog_service.get_blog_by_user(subscriber)
        total_count=await self.subscription_store.get_subscribed_blog_count(subscriber_id=subscriber_blog.id)
        subscribed_blogs = await self.subscription_store.get_paginated_subscribed_blog_addresses(subscriber_id=subscriber_blog.id, page=page, per_page=per_page)
        blog_responses = [
            BlogDetailResponse.model_validate(blog, from_attributes=True) for blog in subscribed_blogs
        ]
        return PaginatedSubscriptionResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            blogs=blog_responses
        )
    
    async def get_paginated_subscriber_blog_address(self, subscribed: User, page: int, per_page: int)->PaginatedSubscriptionResponse:
        """
        나를 구독 중인 블로그들의 정보 반환(페이지네이션)
        """
        subscribed_blog=await self.blog_service.get_blog_by_user(subscribed)

        total_count=await self.subscription_store.get_subscriber_blog_count(subscribed_id=subscribed_blog.id)
        subscriber_blogs = await self.subscription_store.get_paginated_subscriber_blog_addresses(subscribed_id=subscribed_blog.id, page=page, per_page=per_page)

        blog_responses = [
            BlogDetailResponse.model_validate(blog, from_attributes=True) for blog in subscriber_blogs
        ]
        return PaginatedSubscriptionResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            blogs=blog_responses
        )
    
    async def get_subscribed_blog_addresses(self, subscriber: User) -> List[str]:
        """
        내가 구독 중인 블로그들의 주소 이름 반환
        """
        subscriber_blog=await self.blog_service.get_blog_by_user(subscriber)
        if not subscriber_blog:
            raise BlogNotFoundError
        return await self.subscription_store.get_subscribed_blog_addresses(subscriber_blog.id)
    
    async def get_subscriber_blog_addresses(self, subscribed: User) -> List[str]:
        """
        나를 구독한 블로그들의 주소 이름 반환
        """
        subscribed_blog=await self.blog_service.get_blog_by_user(subscribed)
        if not subscribed_blog:
            raise BlogNotFoundError
        return await self.subscription_store.get_subscriber_blog_addresses(subscribed_blog.id)

    async def is_blog_subscribed(self, subscriber_id: int, subscribed_id: int) -> bool:
        """
        특정 블로그가 현재 사용자의 블로그를 구독하고 있는지 여부 확인
        """
        # SubscriptionStore에서 구독 관계 확인
        subscription = await self.subscription_store.get_subscription(subscriber_id, subscribed_id)
        return subscription is not None