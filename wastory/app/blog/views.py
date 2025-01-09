from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from wastory.app.blog.dto.requests import BlogCreateRequest, BlogUpdateRequest
from wastory.app.blog.dto.responses import BlogDetailResponse
from wastory.app.user.models import User
from wastory.app.blog.service import BlogService
from wastory.app.user.views import login_with_header

blog_router = APIRouter()


@blog_router.post("/", status_code=HTTP_201_CREATED)
async def signup(
    user: Annotated[User, Depends(login_with_header)],
    blog_service: Annotated[BlogService, Depends()],
    blog_create_request: BlogCreateRequest
) -> BlogDetailResponse:
    return await blog_service.create_blog(
        user=user,
        name=blog_create_request.address_name
    )

@blog_router.get("/{address_name}")
async def get_blog(
    address_name: str,
    blog_service: Annotated[BlogService, Depends()]
)->BlogDetailResponse:
    return await blog_service.get_blog_by_address_name(address_name=address_name)

@blog_router.patch("/{address_name}")
async def update_blog(
    user: Annotated[User, Depends(login_with_header)],
    address_name: str,
    blog_service: Annotated[BlogService, Depends()],
    blog_update_request: BlogUpdateRequest
) -> BlogDetailResponse:
    return await blog_service.update_blog(address_name=address_name, new_blog_name=blog_update_request.blog_name, new_description=blog_update_request.description)