from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException

from wastory.app.subscription.service import SubscriptionService
from wastory.app.subscription.dto.responses import SubscriptionDetailResponse, PaginatedSubscriptionResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from wastory.app.user.models import User
from wastory.app.blog.service import BlogService
from wastory.app.user.views import login_with_header
from wastory.app.subscription.errors import BlogNotFoundError
from wastory.app.blog.store import BlogStore
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.user.service import UserService

subscription_router = APIRouter()

@subscription_router.post("", status_code=HTTP_201_CREATED)
async def add_subscription(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    subscribed_id: int,  # 구독할 블로그의 주소 이름
) -> SubscriptionDetailResponse:
    """
    새로운 구독 추가 API
    """
    # 구독 대상 블로그의 ID 가져오기
    subscribed_blog = await blog_service.get_blog_by_id(subscribed_id)
    subscriber_blog = await blog_service.get_blog_by_user(user=user)
    if not subscribed_blog or not subscriber_blog:
        raise BlogNotFoundError

    # 구독 추가
    subscription = await subscribe_service.add_subscription(
        subscriber_id=subscriber_blog.id,
        subscribed_id=subscribed_blog.id
    )

    return subscription

@subscription_router.get("/my_subscriptions/{page}", response_model=PaginatedSubscriptionResponse)
async def get_my_subscriptions(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자,
    page: int,
    subscribe_service: Annotated[SubscriptionService, Depends()]
) -> PaginatedSubscriptionResponse:
    """
    내가 구독 중인 블로그들의 정보를 반환하는 API
    """
    per_page = 10
    return await subscribe_service.get_paginated_subscribed_blog_address(
        subscriber=user,
        page=page,
        per_page=per_page
    )

@subscription_router.get("/my_subscribers/{page}", response_model=PaginatedSubscriptionResponse)
async def get_my_subscribers(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    page: int,
    subscribe_service: Annotated[SubscriptionService, Depends()]
) -> PaginatedSubscriptionResponse:
    """
    나를 구독한 블로그들의 정보를 반환하는 API
    """
    per_page=10
    return await subscribe_service.get_paginated_subscriber_blog_address(
        subscribed=user,
        page=page,
        per_page=per_page
    )

@subscription_router.get("/subcriptions/{page}", response_model=PaginatedSubscriptionResponse)
async def get_subscriptions(
    blog_id: int,
    page: int,
    subscribe_service: Annotated[SubscriptionService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    user_service: Annotated[UserService, Depends()]
) -> PaginatedSubscriptionResponse:
    """
    해당 블로그가 구독 중인 블로그들의 정보를 반환하는 API
    """
    per_page=10
    blog = await blog_service.get_blog_by_id(blog_id=blog_id)
    
    if blog is None:
        raise BlogNotFoundError
    
    user= await user_service.get_user_by_id(blog.user_id)
    
    return await subscribe_service.get_paginated_subscribed_blog_address(
        subscriber=user,
        page=page,
        per_page=per_page
    )

@subscription_router.get("/subscribers/{page}", response_model=PaginatedSubscriptionResponse)
async def get_subscribers(
    blog_id: int,
    page: int,
    subscribe_service: Annotated[SubscriptionService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    user_service: Annotated[UserService, Depends()]
) -> PaginatedSubscriptionResponse:
    """
    해당 블로그를 구독하는 블로그들의 정보를 반환하는 API
    """
    per_page=10
    blog = await blog_service.get_blog_by_id(blog_id=blog_id)
    
    if blog is None:
        raise BlogNotFoundError
    
    user= await user_service.get_user_by_id(blog.user_id)
    
    return await subscribe_service.get_paginated_subscriber_blog_address(
        subscribed=user,
        page=page,
        per_page=per_page
    )


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

@subscription_router.get("/is_subscribed", status_code=HTTP_200_OK)
async def is_blog_subscribing(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    subscriber_id: int  # 구독 여부를 확인할 블로그 ID
) -> dict:
    """
    특정 블로그가 내 블로그를 구독하고 있는지 확인하는 API
    """
    # 현재 사용자의 블로그 정보 가져오기
    subscribed_blog = await blog_service.get_blog_by_user(user=user)
    if not subscribed_blog:
        raise BlogNotFoundError

    # 구독 여부 확인
    is_subscribed = await subscribe_service.is_blog_subscribed(subscriber_id, subscribed_blog.id)

    return {"is_subscribed": is_subscribed}

@subscription_router.get("/is_subscribing", status_code=HTTP_200_OK)
async def is_subscribing(
    user: Annotated[User, Depends(login_with_header)],  # 로그인한 사용자
    subscribe_service: Annotated[SubscriptionService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    subscribed_id: int  # 구독 여부를 확인할 블로그 ID
) -> dict:
    """
    현재 사용자가 특정 블로그를 구독하고 있는지 확인하는 API
    """
    # 현재 사용자의 블로그 정보 가져오기
    subscriber_blog = await blog_service.get_blog_by_user(user=user)
    if not subscriber_blog:
        raise BlogNotFoundError

    # 구독 여부 확인
    is_subscribed = await subscribe_service.is_blog_subscribed(
        subscriber_id=subscriber_blog.id,
        subscribed_id=subscribed_id
    )

    return {"is_subscribing": is_subscribed}


