from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, or_, and_, func
from sqlalchemy.orm import Session
from wastory.app.blog.errors import (
    BlogNotFoundError,
    BlognameAlreadyExistsError,
    BlogAlreadyExistsError
)
from wastory.app.blog.models import Blog
from wastory.app.image.store import ImageStore

from wastory.database.annotation import transactional
from wastory.database.connection import SESSION


class BlogStore:
    def __init__(
        self,
        image_store : Annotated[ImageStore, Depends()]
    ) :
        self.image_store = image_store
    
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
        new_default_category_id: int | None,
        new_main_image_URL: str | None
    ) -> Blog:
        # 기존 블로그 검색
        blog = await self.get_blog_by_address_name(address_name)
        if blog is None:
            raise BlogNotFoundError

        # 블로그 이름 업데이트
        if new_blog_name is not None and new_blog_name!=blog.blog_name:
            if await self.get_blog_by_name(new_blog_name):
                raise BlognameAlreadyExistsError
            blog.blog_name = new_blog_name

        # 설명 업데이트
        if description is not None:
            blog.description = description

        if new_default_category_id is not None:
            blog.default_category_id = new_default_category_id
        
        if new_main_image_URL != blog.main_image_url :
            previous_main_image = await self.image_store.get_main_image_of_blog(blog.id)
            if previous_main_image :
                await self.image_store.delete_image(previous_main_image)
            print("A main_image_url :", blog.main_image_url)

            if new_main_image_URL :
                print("B main_image_url :", new_main_image_URL)
                await self.image_store.create_image(
                    file_url = new_main_image_URL, 
                    blog_id = blog.id,
                    is_main = True
                )

        blog.main_image_url=new_main_image_URL


        SESSION.merge(blog)
        await SESSION.flush()
        await SESSION.refresh(blog)


        return blog
    
    async def search_blogs_by_keywords(self, keywords: str, page: int, per_page: int) -> list[Blog]:
        """
        키워드로 블로그 검색
        """
        # 검색어 유효성 확인
        keywords = keywords.strip()
        if not keywords:
            return []

        # 오프셋 계산
        offset_val = (page - 1) * per_page

        # 검색어를 공백으로 분리
        words = keywords.split()

        # 이름과 설명 중 하나라도 단어를 포함해야 함
        search_conditions = [
            or_(
                Blog.blog_name.ilike(f"%{word}%"),
                Blog.description.ilike(f"%{word}%")
            )
            for word in words
        ]

        # 조건에 따른 쿼리 작성
        query = (
            select(Blog)
            .where(and_(*search_conditions))  # 하나라도 매칭되는 경우 반환
            .offset(offset_val)
            .limit(per_page)
        )

        # 쿼리 실행
        results = await SESSION.scalars(query)
        return list(results)
    
    async def count_search_result_by_keywords(self, keywords: str)-> int:
         # 검색어 유효성 확인
        keywords = keywords.strip()
        if not keywords:
            return 0

        # 검색어를 공백으로 분리
        words = keywords.split()

        # 검색 조건 생성
        search_conditions = [
            or_(
                Blog.blog_name.ilike(f"%{word}%"),
                Blog.description.ilike(f"%{word}%")
            )
            for word in words
        ]

        # 검색 조건 결합
        query = (
            select(func.count(Blog.id))
            .where(and_(*search_conditions))  # 모든 검색 조건 충족
        )

        # 쿼리 실행 및 결과 반환
        count = await SESSION.scalar(query)
        return count or 0