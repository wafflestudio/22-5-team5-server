from functools import cache
from typing import Annotated

from sqlalchemy import select,and_
from wastory.app.comment.errors import CommentNotFoundError,NotOwnerError
from wastory.app.user.models import User
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.category.models import Category
from wastory.app.article.models import Article
from wastory.app.comment.models import Comment

class CommentStore:
    async def get_comment_by_id(self,id:int)->Comment|None:
        get_comment_query=select(Comment).filter(Comment.id==id)
        comment=await SESSION.scalar(get_comment_query)
        return comment

    @transactional
    async def create_comment_1(
        self, content:str,secret:int,user:User,article:Article,article_id:int
        )->Comment:
            comment= Comment(
                content=content,
                level=1,
                secret=secret,
                user=user,
                user_id=user.id,
                article=article,
                article_id=article_id,
                parent_id=None
                )
            SESSION.add(comment)
            await SESSION.flush()
            await SESSION.refresh(comment)
            return comment
        
    @transactional
    async def create_comment_2(
        self, content:str,secret:int,user:User,article:Article,parent_id:int
        )->Comment:
            comment= Comment(
                content=content,
                level=2,
                secret=secret,
                user=user,
                user_id=user.id,
                article=article,
                article_id=article.id,
                parent_id=parent_id
            )
            parent_comment=await self.get_comment_by_id(parent_id)
            if not parent_comment:
                raise CommentNotFoundError()
            comment.parent = parent_comment
            SESSION.add(comment)
            await SESSION.flush()
            await SESSION.refresh(comment)
            return comment






    async def get_category_of_blog(self,blog_id:int)->list[Category]|None:
        get_category_query=select(Category).filter(
            Category.blog_id==blog_id
        )
        categories=await SESSION.scalars(get_category_query)
        return categories

    @transactional
    async def update_comment(
        self,
        user:User,
        comment_id: int,
        content:str
    ) -> Comment:
        comment = await self.get_comment_by_id(comment_id)
        
        
        if comment is None:
            raise CommentNotFoundError()

        if comment.user_id!=user.id:
            raise NotOwnerError()

        if content is not None:
            comment.content=content
        

        SESSION.merge(comment)
        await SESSION.flush()
        await SESSION.refresh(comment)

        return comment

    @transactional
    async def delete_comment(self, user: User, comment_id: int) -> None:
        comment = await self.get_comment_by_id(comment_id)

        if comment is None:
            raise CommentNotFoundError()

        
        #if category.blog_id != user.blogs.id:
        #   raise NotOwnerError()

        # 카테고리 삭제
        await SESSION.delete(comment)
        await SESSION.flush()

    