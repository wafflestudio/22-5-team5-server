from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wastory.app.blog.errors import (
    BlogNotFoundError,
    BlognameAlreadyExistsError,
    BlogAlreadyExistsError
)
from wastory.app.blog.models import Blog
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION


class BlogStore:
    @transactional
    async def add_blog(self, user_id: int, name : str, default_id : int) -> Blog:
        blog_name = name + "님의 블로그"
        description = name + "님의 블로그입니다."
        if await self.get_blog_by_name(blog_name):
            raise BlognameAlreadyExistsError
        if await self.get_blog_of_user(user_id=user_id):
            raise BlogAlreadyExistsError
        blog=Blog(
            address_name=name,
            description=description,
            blog_name=blog_name,
            user_id=user_id,
            default_category_id=default_id
        )
        SESSION.add(blog)
        await SESSION.flush()
        await SESSION.refresh(blog)
        return blog
    

    async def get_blog_by_id(self, blog_id: int) -> Blog | None:
        get_blog_query = select(Blog).filter(Blog.id == blog_id)
        blog = await SESSION.scalar(get_blog_query)
        return blog


    async def get_blog_of_user(self, user_id: int) -> Blog | None:
        get_blog_query = select(Blog).filter(Blog.user_id == user_id)
        blog = await SESSION.scalar(get_blog_query)
        return blog


    async def get_blog_by_address_name(self, name: str) -> Blog | None:
        get_blog_query = select(Blog).filter(Blog.address_name == name)
        blog = await SESSION.scalar(get_blog_query)
        if blog:
            print(f"Debug: Blog={blog}", flush=True)
            print(f"main_image_url: {blog.main_image_url}", flush=True)
        return blog
    

    async def get_blog_by_name(self, name: str) -> Blog | None:
        get_blog_query = select(Blog).filter(Blog.blog_name == name)
        blog = await SESSION.scalar(get_blog_query)
        return blog

    @transactional
    async def update_blog(
        self,
        address_name: str,
        new_blog_name: str | None,
        description: str | None,
        new_default_category_id: int | None
    ) -> Blog:
        # 기존 블로그 검색
        blog = await self.get_blog_by_address_name(address_name)
        if blog is None:
            raise BlogNotFoundError

        # 블로그 이름 업데이트
        if new_blog_name is not None:
            if await self.get_blog_by_name(new_blog_name):
                raise BlognameAlreadyExistsError
            blog.blog_name = new_blog_name

        # 설명 업데이트
        if description is not None:
            blog.description = description

        if new_default_category_id is not None:
            blog.default_category_id = new_default_category_id
        SESSION.merge(blog)
        await SESSION.flush()
        await SESSION.refresh(blog)


        return blog
