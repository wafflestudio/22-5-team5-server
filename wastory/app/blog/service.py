from typing import Annotated

from fastapi import Depends
from wastory.app.blog.models import Blog
from wastory.app.user.models import User
from wastory.app.blog.store import BlogStore
from wastory.app.blog.dto.responses import BlogDetailResponse
from wastory.app.blog.errors import BlogNotFoundError


class BlogService:
    def __init__(self, blog_store: Annotated[BlogStore, Depends()]) -> None:
        self.blog_store = blog_store

    async def create_blog(
        self,
        user : User,
        name : str,
    ) -> BlogDetailResponse:
        
        blog = await self.blog_store.add_blog(user_id=user.id, name=name)

        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def get_blog_by_id(self, blog_id : int) -> BlogDetailResponse:
        blog=await self.blog_store.get_blog_by_id(blog_id)
        if blog is None:
            raise BlogNotFoundError
        return BlogDetailResponse.model_validate(blog, from_attributes=True)
    
    async def get_blog_by_name(self, blog_name : str) -> BlogDetailResponse:
        blog=await self.blog_store.get_blog_by_name(blog_name)
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
        blog_name : str,
        new_blog_name : str | None,
        new_description : str |None
    ) -> BlogDetailResponse:
        updated_blog = await self.blog_store.update_blog(
            blog_name=blog_name,
            new_blog_name=new_blog_name,
            description=new_description
        )
        return BlogDetailResponse.model_validate(updated_blog, from_attributes=True)