from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException

from wastory.app.subscription.service import SubscriptionService
from wastory.app.subscription.dto.responses import SubscriptionDetailResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from wastory.app.user.models import User
from wastory.app.blog.service import BlogService
from wastory.app.user.views import login_with_header
from wastory.app.subscription.errors import BlogNotFoundError

subscription_router = APIRouter()

@subscription_router.post("", status_code=HTTP_201_CREATED)
async def add_subscription(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    subscribed_address_name: str,  # 구독할 블로그의 주소 이름
) -> SubscriptionDetailResponse:
    """
    새로운 구독 추가 API
    """
    # 구독 대상 블로그의 ID 가져오기
    subscribed_blog = await blog_service.get_blog_by_address_name(subscribed_address_name)
    subscriber_blog = await blog_service.get_blog_by_user(user=user)
    if not subscribed_blog or not subscriber_blog:
        raise BlogNotFoundError

    # 구독 추가
    subscription = await subscribe_service.add_subscription(
        subscriber_id=subscriber_blog.id,
        subscribed_id=subscribed_blog.id
    )

    return subscription

@subscription_router.get("/my_subscriptions", response_model=List[str])
async def get_my_subscriptions(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()]
) -> List[str]:
    """
    내가 구독 중인 블로그들의 주소 이름을 반환하는 API
    """
    return await subscribe_service.get_subscribed_blog_addresses(user.id)

@subscription_router.get("/my_subscribers", response_model=List[str])
async def get_my_subscribers(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()]
) -> List[str]:
    """
    나를 구독한 블로그들의 주소 이름을 반환하는 API
    """
    return await subscribe_service.get_subscriber_blog_addresses(user.id)

@subscription_router.delete("", status_code=HTTP_200_OK)
async def cancel_subscription(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()],
    subscribed_address_name: str,  # 구독 취소할 블로그의 주소 이름
):
    """
    구독 취소 API
    """
    await subscribe_service.cancel_subscription(subscriber_user=user, subscribed_address_name=subscribed_address_name)

    return {"message": "Subscription canceled successfully."}