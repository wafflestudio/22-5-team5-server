from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select,and_
from sqlalchemy.orm import Session
from wastory.app.category.errors import CategoryNameDuplicateError,CategoryNotFoundError,NotOwnerError
from wastory.app.user.models import User
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.category.models import Category
from wastory.app.blog.models import Blog

class CategoryStore:

    @transactional
    async def create_category(
        self, blog:Blog,categoryname:str, categorylevel:int, parentId:int|None=None
        )->Category:
            category= Category(blog=blog,blog_id=blog.id,name=categoryname,level=categorylevel,parent_id=parentId)
            SESSION.add(category)
            await SESSION.flush()
            return category
        

    async def get_category_by_categoryname(self, name:str) ->Category|None:
        get_category_query=select(Category).filter(Category.name==name)
        category=await SESSION.scalar(get_category_query)
        return category

    async def get_category_by_id(self, id:int)->Category|None:
        get_category_query=select(Category).filter(Category.id==id)
        category=await SESSION.scalar(get_category_query)
        return category

    #여기가 많은 개선이 필요함!!
    async def get_category_by_name_parent_level(self,new_category_name:str,parentId:int, level:int)->Category|None:
        get_category_query = select(Category).filter(
            and_(
                Category.name == new_category_name,
                Category.level == level,
                Category.parent_id == parentId  # parent가 User 객체라면 .id로 비교
            )
        )
        category=await SESSION.scalar(get_category_query)
        return category

    async def get_categories_by_user(self,blog:Blog)->list[Category]|None:
        get_category_query=select(Category).filter(
            and_(
                Category.blog==blog,
                Category.level==1
            )
        )
        categories=await SESSION.scalars(get_category_query)
        return categories

    @transactional
    async def update_category(
        self,
        user:User,
        category_id: int,
        new_cateogry_name:str
    ) -> Category:
        category = await self.get_category_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError()

        if category.blog !=user.blog:
            raise NotOwnerError()

        if new_cateogry_name is not None:
            if await self.get_category_by_name_parent_level(
                new_cateogry_name,
                category.parent_id,
                category.level
                ): 
                raise CategoryNameDuplicateError()
            category.name=new_cateogry_name

        SESSION.merge(category)
        await SESSION.flush()
        await SESSION.refresh(category)

        return category

    @transactional
    async def delete_category(self, user: User, category_id: int) -> None:
        category = await self.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()

        if category.blog != user.blog:
            raise NotOwnerError()

        # 카테고리 삭제
        SESSION.delete(category)
        await SESSION.flush()

    