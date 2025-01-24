from functools import cache
from typing import Annotated
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy import select,and_
from wastory.app.category.errors import CategoryNameDuplicateError,CategoryNotFoundError,NotOwnerError
from wastory.app.user.models import User
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.category.models import Category
from wastory.app.article.models import Article

class CategoryStore:

    @transactional
    async def create_category(
        self, blog_id:int,categoryname:str, categorylevel:int, parentId:int|None=None
        )->Category:
            if await self.get_category_by_blog_and_name(blog_id=blog_id,name=categoryname):
                raise CategoryNameDuplicateError()
            category= Category(
                blog_id=blog_id,
                name=categoryname,
                level=categorylevel,
                parent_id=parentId,
                children=[]
                )
            SESSION.add(category)
            await SESSION.flush()
            await SESSION.refresh(category)
            return category
        
    async def get_category_by_blog_and_name(self, blog_id: int, name: str) -> Category | None:
        stmt = (
            select(Category)
            .filter(Category.blog_id == blog_id)
            .filter(Category.name == name)
        )
        category = await SESSION.scalar(stmt)
        return category

    async def get_category_by_categoryname(self, name:str) ->Category|None:
        get_category_query=select(Category).filter(Category.name==name)
        category=await SESSION.scalar(get_category_query)
        return category
    
    async def get_article_count(self, category_id: int) -> int:
        stmt = select(func.count(Article.id)).filter(Article.category_id == category_id)
        count = await SESSION.scalar(stmt)
        return count or 0
        
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



    async def get_category_of_blog(self,blog_id:int)->list[Category]|None:
        get_category_query=select(Category).filter(
            Category.blog_id==blog_id
        )
        stmt=(
            select(Category)
            .filter(Category.blog_id==blog_id, Category.level==1)
            .options(selectinload(Category.children))
        )
        categories=await SESSION.scalars(stmt)
        return list(categories)

    @transactional
    async def update_category(
        self,
        user:User,
        category_id: int,
        new_category_name:str
    ) -> Category:
        category = await self.get_category_by_id(category_id)
        
        
        if category is None:
            raise CategoryNotFoundError()

        if category.blog !=user.blog:
            raise NotOwnerError()

        if new_category_name is not None:
            if await self.get_category_by_name_parent_level(
                new_cateogry_name=new_category_name,
                parentId=category.parent_id,
                level=category.level
                ): 
                raise CategoryNameDuplicateError()
        
        category.name=new_category_name
        

        SESSION.merge(category)
        await SESSION.flush()
        await SESSION.refresh(category)

        return category

    @transactional
    async def delete_category(self, user: User, category_id: int) -> None:
        category = await self.get_category_by_id(category_id)
        print(category)

        if category is None:
            raise CategoryNotFoundError()

        
        #if category.blog_id != user.blogs.id:
        #   raise NotOwnerError()

        # 카테고리 삭제
        await SESSION.delete(category)
        await SESSION.flush()

    