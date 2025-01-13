from fastapi import Depends
from sqlalchemy import select
from wastory.app.subscription.models import Subscription
from wastory.app.blog.models import Blog
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.subscription.errors import (
    SubscriptionAlreadyExistsError,
    BlogNotFoundError,
)


class SubscriptionStore:
    @transactional
    async def add_subscription(self, subscriber_id: int, subscribed_id: int) -> Subscription:
        """
        구독 추가 기능: 특정 블로그가 다른 블로그를 구독합니다.
        """
        # 구독할 블로그와 구독자가 존재하는지 확인
        subscriber_blog = await SESSION.scalar(select(Blog).filter(Blog.id == subscriber_id))
        subscribed_blog = await SESSION.scalar(select(Blog).filter(Blog.id == subscribed_id))

        if not subscriber_blog or not subscribed_blog:
            raise BlogNotFoundError("Subscriber or Subscribed blog not found")

        # 이미 존재하는 구독 관계인지 확인
        existing_subscription_query = select(Subscription).filter(
            Subscription.subscriber_id == subscriber_id,
            Subscription.subscribed_id == subscribed_id,
        )
        existing_subscription = await SESSION.scalar(existing_subscription_query)
        if existing_subscription:
            raise SubscriptionAlreadyExistsError("Subscription already exists")

        # 새로운 구독 생성
        subscription = Subscription(
            subscriber_id=subscriber_id,
            subscribed_to_id=subscribed_id,
        )
        SESSION.add(subscription)
        await SESSION.flush()
        await SESSION.refresh(subscription)

        return subscription
