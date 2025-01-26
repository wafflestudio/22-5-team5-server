from typing import Annotated

from fastapi import Depends
from wastory.app.blog.models import Blog
from wastory.app.user.models import User
from wastory.app.blog.store import BlogStore
from wastory.app.blog.dto.responses import BlogDetailResponse, PaginatedBlogDetailResponse
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.user.store import UserStore
from wastory.app.category.store import CategoryStore


class BlogService:
    def __init__(self, blog_store: Annotated[BlogStore, Depends()], user_store: Annotated[UserStore, Depends()], category_store: Annotated[CategoryStore, Depends()]) -> None:
        self.blog_store = blog_store
        self.user_store = user_store
        self.categroy_store = category_store

    async def create_blog(
        self,
        user : User,
        name : str,
    ) -> BlogDetailResponse:

        await self.user_store.update_user(username=name, email=user.email, nickname=None)

        blog = await self.blog_store.add_blog(user_id=user.id, name=name, default_id=0)

        default_category=await self.categroy_store.create_category(blog_id=blog.id, categoryname="카테고리 없음", categorylevel=1)
        print(default_category.id)
        await self.blog_store.update_blog(address_name=blog.address_name, new_default_category_id=default_category.id, new_blog_name=None, description=None, new_main_image_URL=None)

        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def get_blog_by_id(self, blog_id : int) -> BlogDetailResponse:
        blog=await self.blog_store.get_blog_by_id(blog_id)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def get_blog_by_address_name(self, address_name : str) -> BlogDetailResponse:
        blog=await self.blog_store.get_blog_by_address_name(address_name)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)

    async def get_blog_by_user(self, user : User) -> BlogDetailResponse:
        blog = await self.blog_store.get_blog_of_user(user.id)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)

    async def update_blog(
        self,
        address_name : str,
        new_blog_name : str | None,
        new_description : str |None,
        new_default_category_id : int|None,
        new_main_image_URL : str | None
    ) -> BlogDetailResponse:
        updated_blog = await self.blog_store.update_blog(
            address_name=address_name,
            new_blog_name=new_blog_name,
            description=new_description,
            new_default_category_id=new_default_category_id,
            new_main_image_URL=new_main_image_URL
        )
        return BlogDetailResponse.model_validate(updated_blog, from_attributes=True)
    
    async def get_blog_by_user_email(self, email: str) -> BlogDetailResponse:
        """
        이메일을 통해 유저의 블로그 조회
        """
        # 이메일로 유저 정보 조회
        user = await self.user_store.get_user_by_email(email)
        if not user:
            raise BlogNotFoundError

        # 유저의 블로그 조회
        blog = await self.blog_store.get_blog_of_user(user_id=user.id)
        if not blog:
            raise BlogNotFoundError

        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def search_blog_by_keywords(self, keywords: str, page: int, per_page: int) -> PaginatedBlogDetailResponse:
        """
        키워드로 블로그 검색
        """
        # 검색된 블로그와 총 개수를 반환
        blogs = await self.blog_store.search_blogs_by_keywords(keywords, page, per_page)
        total_count = await self.blog_store.count_search_result_by_keywords(keywords)

        # 블로그 목록을 DTO로 변환
        blog_responses = [
            BlogDetailResponse.model_validate(blog, from_attributes=True) for blog in blogs
        ]

        # 페이지네이션 응답 생성
        return PaginatedBlogDetailResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            blogs=blog_responses,
        )