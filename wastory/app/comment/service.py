from typing import Annotated, Optional

from fastapi import Depends
from wastory.app.comment.store import CommentStore
from wastory.app.comment.dto.responses import CommentDetailResponse,CommentListResponse,PaginatedCommentListResponse
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.user.models import User
from wastory.app.user.store import UserStore
from wastory.app.article.store import ArticleStore
from wastory.app.blog.store import BlogStore
class CommentService:
    def __init__(
        self, 
        comment_store: Annotated[CommentStore, Depends()],
        user_store:Annotated[UserStore,Depends()],
        article_store:Annotated[ArticleStore,Depends()],
        blog_store:Annotated[BlogStore,Depends()]) -> None:
        self.comment_store = comment_store
        self.user_store=user_store
        self.article_store=article_store
        self.blog_store=blog_store


    async def create_article_comment(
        self, content:str,level:int,secret:int,user:User,article_id:int,parent_id:int
        )-> CommentDetailResponse:
            #article id를 받아서, article 을 받고 넘기자
            article=await self.article_store.get_article_by_id(article_id)
            if article==None:
                raise ArticleNotFoundError()
            if level==1:
                new_comment=await self.comment_store.create_article_comment_1(
                    content=content,
                    secret=secret,
                    user=user,
                    
                    article_id=article_id
                )
            elif level==2:
                new_comment=await self.comment_store.create_article_comment_2(
                    content=content,
                    secret=secret,
                    user=user,
                    article_id=article_id,
                    parent_id=parent_id
                )
            return CommentDetailResponse.from_comment(new_comment,user)

    async def create_guestbook_comment(
        self, content:str,level:int,secret:int,user:User,blog_id:int,parent_id:int
        )-> CommentDetailResponse:
            #article id를 받아서, article 을 받고 넘기자
            blog=await self.blog_store.get_blog_by_id(blog_id)
            if blog==None:
                raise BlogNotFoundError()   ##바꿔야 해
            if level==1:
                new_comment=await self.comment_store.create_guestbook_comment_1(
                    content=content,
                    secret=secret,
                    user=user,
                    blog_id=blog_id
                )
            elif level==2:
                new_comment=await self.comment_store.create_guestbook_comment_2(
                    content=content,
                    secret=secret,
                    user=user,
                    blog_id=blog_id,
                    parent_id=parent_id
                )
            return CommentDetailResponse.from_comment(new_comment,user)

    async def update_comment(
        self,user:User,comment_id:int,content:str
    )-> CommentDetailResponse:
        comment=await self.comment_store.update_comment(
            user=user,
            comment_id=comment_id,
            content=content
        )
        return CommentDetailResponse.from_comment(comment,user)

    async def delete_comment(
        self, user:User, comment_id:int
    )-> None:
        await self.comment_store.delete_comment(
            user=user,
            comment_id=comment_id
        )
    '''
    async def get_article_list_level1_with_children(
        self,
        article_id: int,
        page: int,
        per_page: int
    ) -> list[CommentListResponse]:
        """
        page, per_page에 맞춰 level=1 댓글은 페이지네이션, 
        각 댓글의 children은 전부 포함.
        """
        # store에서 level=1 댓글들만 가져옴 (limit/offset)
        level1_comments = await self.comment_store.get_article_comments(
            article_id=article_id, 
            page=page, 
            per_page=per_page
        )

        # DTO 변환
        return [CommentListResponse.from_comment(c) for c in level1_comments]
    '''
    # 페이지네이션 정보를 추가로 내려주고 싶으면
    async def get_article_list_pagination(
        self,
        article_id: int,
        page: int,
        per_page: int,
        current_user: Optional[User] = None  # ← 추가
    ) -> PaginatedCommentListResponse:
        total_count = await self.comment_store.get_article_comments_count(article_id)
        level1_comments = await self.comment_store.get_article_comments(
            article_id=article_id, 
            page=page, 
            per_page=per_page
        )

        # 현재 유저를 `from_comment`에 넘겨주어야 함
        comments_list = [
            CommentListResponse.from_comment(c, current_user)
            for c in level1_comments
        ]

        return PaginatedCommentListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            comments=comments_list
        )
    

    '''
    async def get_guestbook_list_level1_with_children(
        self,
        blog_id: int,
        page: int,
        per_page: int
    ) -> list[CommentListResponse]:
        """
        page, per_page에 맞춰 level=1 댓글은 페이지네이션, 
        각 댓글의 children은 전부 포함.
        """
        # store에서 level=1 댓글들만 가져옴 (limit/offset)
        level1_comments = await self.comment_store.get_guestbook_comments(
            blog_id=blog_id, 
            page=page, 
            per_page=per_page
        )

        # DTO 변환
        return [CommentListResponse.from_comment(c) for c in level1_comments]
    '''
    # 페이지네이션 정보를 추가로 내려주고 싶으면
    async def get_guestbook_list_pagination(
        self,
        blog_id: int,
        page: int,
        per_page: int,
        current_user: Optional[User] = None  # ← 추가
    ) -> PaginatedCommentListResponse:
        total_count = await self.comment_store.get_guestbook_comments_count(article_id)
        level1_comments = await self.comment_store.get_guestbook_comments(
            blog_id=blog_id, 
            page=page, 
            per_page=per_page
        )

        # 현재 유저를 `from_comment`에 넘겨주어야 함
        comments_list = [
            CommentListResponse.from_comment(c, current_user)
            for c in level1_comments
        ]

        return PaginatedCommentListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count,
            comments=comments_list
        )