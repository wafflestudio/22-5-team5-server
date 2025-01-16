from typing import Annotated
from fastapi import APIRouter, Depends
from wastory.app.like.dto.requests import LikeCreateRequest
from wastory.app.like.dto.responses import LikeDetailInListResponse, LikeDetailResponse
from wastory.app.like.service import LikeService
from wastory.app.blog.service import BlogService

from wastory.app.user.models import User
from wastory.app.user.views import login_with_header


like_router = APIRouter()

# like 생성
@like_router.post("/create", status_code=201)
async def create_like(
    user: Annotated[User, Depends(login_with_header)],
    blog_service: Annotated[BlogService, Depends()],
    like_service: Annotated[LikeService, Depends()],
    like: LikeCreateRequest,
) -> LikeDetailResponse:
    user_blog = await blog_service.get_blog_by_user(user)

    return await like_service.create_like(user, user_blog.id, like.article_id)

# like 삭제
@like_router.delete("/{like_id}", status_code=204)
async def delete_like(
    user: Annotated[User, Depends(login_with_header)],
    like_id: int,
    like_service: Annotated[LikeService, Depends()],
) -> None:
    await like_service.delete_like(user, like_id)


# blog 가 누른 like 조회
@like_router.get("/blog/{blog_id}", status_code=200)
async def get_likes_by_blog(
    like_service: Annotated[LikeService, Depends()],
    blog_id : int,
) -> list[LikeDetailInListResponse]:
    return await like_service.get_likes_by_blog(blog_id)

# article 이 받은 like 조회
@like_router.get("/article/{article_id}", status_code=200)
async def get_likes_in_article(
    like_service: Annotated[LikeService, Depends()],
    article_id : int,
) -> list[LikeDetailInListResponse]:
    return await like_service.get_likes_in_article(article_id)

# service 상에서 구현된 method 는 특정 blog 에서 특정 article 에 like 가 존재하는지를 확인
# 해당 method 를 이용해서 user 가 login 한 자신의 blog 에서 like 를 눌렀는지 확인
@like_router.get("/blog/press_like/{article_id}", status_code=200)
async def blog_press_like(
    user: Annotated[User, Depends(login_with_header)],
    like_service: Annotated[LikeService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
    article_id: int,
) -> bool:
    user_blog = await blog_service.get_blog_by_user(user)
    return await like_service.blog_press_like(user_blog.id, article_id)