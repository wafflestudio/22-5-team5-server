from typing import Annotated
from fastapi import Depends
from wastory.app.subscription.store import SubscriptionStore
from wastory.app.subscription.dto.responses import SubscriptionDetailResponse


class SubscriptionService:
    def __init__(self, subscription_store: Annotated[SubscriptionStore, Depends()]) -> None:
        self.subscription_store = subscription_store

    async def add_subscription(self, subscriber_id: int, subscribed_id: int) -> SubscriptionDetailResponse:
        """
        구독 추가 서비스
        """
        # SubscriptionStore에서 구독 추가 호출
        subscription = await self.subscription_store.add_subscription(subscriber_id, subscribed_id)

        # SubscriptionDetailResponse로 변환하여 반환
        return SubscriptionDetailResponse.model_validate(subscription, from_attributes=True)
