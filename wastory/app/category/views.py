from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,HTTP_204_NO_CONTENT

from wastory.app.category.dto.requests import CategoryUpdateRequest,CategoryCreateRequest
from wastory.app.category.dto.responses import CategoryDetailResponse,CategoryListResponse,CategoryFinalResponse
from wastory.app.category.models import Category
from wastory.app.category.service import CategoryService
from wastory.app.user.models import User
category_router = APIRouter()
from wastory.app.user.views import login_with_header,optional_login_with_header

#카테고리를 생성하는 API
@category_router.post("/create", status_code=HTTP_201_CREATED)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    category_create_request:CategoryCreateRequest,
    category_service: Annotated[CategoryService, Depends()],
)-> CategoryDetailResponse:
    print(category_create_request.categoryname)
    return await category_service.create_category(
        user=user,
        categoryname=category_create_request.categoryname, 
        categorylevel=category_create_request.categoryLevel,
        parentId=category_create_request.parent_id
    )

#현재 유저가 지니고 있는 카테고리들을 불러오는 API
@category_router.get("/list", status_code=HTTP_200_OK)
async def get_list(
    user:Annotated[User,Depends(optional_login_with_header)],
    category_service:Annotated[CategoryService,Depends()],
)-> CategoryFinalResponse:
    return await category_service.list_categories(user)

#특정 카테고리의 이름을 바꾸는 API
@category_router.patch("/{category_id}", status_code=HTTP_200_OK)
async def update_category(
    user: Annotated[User, Depends(login_with_header)],
    category_id:int,
    update_request: CategoryUpdateRequest,
    category_service: Annotated[CategoryService, Depends()],
)-> CategoryDetailResponse:
    return await category_service.update_category(
        user=user,
        category_id=category_id,
        new_category_name=update_request.categoryname
    )

@category_router.delete("/{category_id}",status_code=HTTP_204_NO_CONTENT)
async def delete_category(
    user:Annotated[User,Depends(login_with_header)],
    category_id:int,
    category_service:Annotated[CategoryService,Depends()],
)-> None:
    await category_service.delete_category(user,category_id)
    
