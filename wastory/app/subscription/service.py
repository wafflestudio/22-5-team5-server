from typing import Annotated, List
from fastapi import Depends
from wastory.app.subscription.store import SubscriptionStore
from wastory.app.subscription.dto.responses import SubscriptionDetailResponse
from wastory.app.blog.service import BlogService
from wastory.app.subscription.errors import BlogNotFoundError
from wastory.app.user.models import User


class SubscriptionService:
    def __init__(self, subscription_store: Annotated[SubscriptionStore, Depends()], blog_service: Annotated[BlogService, Depends()]) -> None:
        self.subscription_store = subscription_store
        self.blog_service=blog_service

    async def add_subscription(self, subscriber_id: int, subscribed_id: int) -> SubscriptionDetailResponse:
        """
        구독 추가 서비스
        """
        # SubscriptionStore에서 구독 추가 호출
        subscription = await self.subscription_store.add_subscription(subscriber_id, subscribed_id)

        # SubscriptionDetailResponse로 변환하여 반환
        return SubscriptionDetailResponse.model_validate(subscription, from_attributes=True)
    
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
