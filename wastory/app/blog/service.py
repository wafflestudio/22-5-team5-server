from typing import Annotated

from fastapi import Depends
from wastory.app.blog.models import Blog
from wastory.app.user.models import User
from wastory.app.blog.store import BlogStore
from wastory.app.blog.dto.responses import BlogDetailResponse
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

        await self.user_store.update_username(username=name, email=user.email)

        blog = await self.blog_store.add_blog(user_id=user.id, name=name, default_id=0)

        default_category=await self.categroy_store.create_category(blog_id=blog.id, categoryname="카테고리 없음", categorylevel=1)

        await self.blog_store.update_blog(address_name=blog.address_name, new_default_category_id=default_category.id, new_blog_name=None, description=None)

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
        new_default_category_id : int|None
    ) -> BlogDetailResponse:
        updated_blog = await self.blog_store.update_blog(
            address_name=address_name,
            new_blog_name=new_blog_name,
            description=new_description,
            new_default_category_id=new_default_category_id
        )
        return BlogDetailResponse.model_validate(updated_blog, from_attributes=True)