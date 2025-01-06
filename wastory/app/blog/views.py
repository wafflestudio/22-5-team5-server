from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from wastory.app.blog.dto.requests import BlogCreateRequest
from wastory.app.blog.dto.responses import BlogDetailResponse
from wastory.app.user.models import User
from wastory.app.blog.service import BlogService
from wastory.app.user.views import login_with_header

blog_router = APIRouter()


@blog_router.post("/create", status_code=HTTP_201_CREATED)
async def signup(
    user: Annotated[User, Depends(login_with_header)],
    blog_service: Annotated[BlogService, Depends()],
    blog_create_request: BlogCreateRequest
) -> BlogDetailResponse:
    return await blog_service.create_blog(
        user=user,
        name=blog_create_request.blog_name,
        description=blog_create_request.description
    )

@blog_router.get("/{blog_name}")
async def get_blog(
    blog_name: str,
    blog_service: Annotated[BlogService, Depends()]
)->BlogDetailResponse:
    return await blog_service.get_blog_by_name(blog_name=blog_name)

@blog_router.patch("/{blog_name}")
async def update_blog(
    user: Annotated[User, Depends(login_with_header)],
    
)

@user_router.get("/me", status_code=HTTP_200_OK)
async def me(user: Annotated[User, Depends(login_with_header)]) -> MyProfileResponse:
    return MyProfileResponse.from_user(user)


@user_router.patch("/me", status_code=HTTP_200_OK)
async def update_me(
    user: Annotated[User, Depends(login_with_header)],
    update_request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends()],
):
    await user_service.update_user(
        user.username,
        email=update_request.email,
        address=update_request.address,
        phone_number=update_request.phone_number,
    )
    return "Success"