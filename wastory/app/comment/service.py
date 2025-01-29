from typing import Annotated, Optional

from fastapi import Depends
from wastory.app.comment.store import CommentStore
from wastory.app.comment.dto.responses import CommentDetailResponse,CommentListResponse,PaginatedCommentListResponse
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.user.models import User
from wastory.app.user.store import UserStore
from wastory.app.article.store import ArticleStore
from wastory.app.notification.service import NotificationService
from wastory.app.blog.store import BlogStore
class CommentService:
    def __init__(
        self, 
        comment_store: Annotated[CommentStore, Depends()],
        user_store:Annotated[UserStore,Depends()],
        article_store:Annotated[ArticleStore,Depends()],
        notification_service:Annotated[NotificationService,Depends()],
        blog_store:Annotated[BlogStore,Depends()]) -> None:
        self.comment_store = comment_store
        self.user_store=user_store
        self.article_store=article_store
        self.notification_service=notification_service
        self.blog_store=blog_store


    async def create_article_comment(
        self, content:str,level:int,secret:int,user:User,article_id:int,parent_id:int
        )-> CommentDetailResponse:
            #article id를 받아서, article 을 받고 넘기자
            article=await self.article_store.get_article_by_id(article_id)
            blog=await self.blog_store.get_blog_by_id(article.blog_id)
            user_blog=await self.blog_store.get_blog_of_user(user.id)
            if article==None:
                raise ArticleNotFoundError()
            if level==1:
                new_comment=await self.comment_store.create_article_comment_1(
                    content=content,
                    secret=secret,
                    user=user,
                    
                    article_id=article_id
                )
                # 댓글 알림
                if (blog.user_id != user.id):
                    await self.notification_service.add_notification(
                        blog_address_names = [blog.address_name],
                        username=user.username,
                        type = 3,
                        notification_blog_name = blog.blog_name,
                        notification_blog_image_url = user_blog.main_image_url,
                        article_id=article.id,
                        comment_id = new_comment.id
                    )
            elif level==2:
                new_comment=await self.comment_store.create_article_comment_2(
                    content=content,
                    secret=secret,
                    user=user,
                    article_id=article_id,
                    parent_id=parent_id
                )
                # 댓글 알림
                await self.notification_service.add_notification(
                    blog_address_names = await self.comment_store.get_replies_blog_address_name(user_blog.address_name, parent_id),
                    type = 3,
                    notification_blog_name = blog.blog_name,
                    username=user.username,
                    notification_blog_image_url = user_blog.main_image_url,
                    article_id=article.id,
                    comment_id = new_comment.id
                )
            return CommentDetailResponse.from_comment(new_comment, user)

    async def create_guestbook_comment(
        self, content:str,level:int,secret:int,user:User,blog_id:int,parent_id:int
        )-> CommentDetailResponse:
            #article id를 받아서, article 을 받고 넘기자
            blog=await self.blog_store.get_blog_by_id(blog_id)
            user_blog=await self.blog_store.get_blog_of_user(user.id)
            if blog==None:
                raise BlogNotFoundError()   ##바꿔야 해
            if level==1:
                new_comment=await self.comment_store.create_guestbook_comment_1(
                    content=content,
                    secret=secret,
                    user=user,
                    blog_id=blog_id
                )
                # 방명록 알림
                if (blog.user_id != user.id):
                    await self.notification_service.add_notification(
                        blog_address_names = [blog.address_name],
                        username=user.username,
                        type=4,
                        notification_blog_name=blog.blog_name,
                        notification_blog_image_url=user_blog.main_image_url,
                        comment_id=new_comment.id
                    )
            elif level==2:
                new_comment=await self.comment_store.create_guestbook_comment_2(
                    content=content,
                    secret=secret,
                    user=user,
                    blog_id=blog_id,
                    parent_id=parent_id
                )
                # 방명록 알림
                await self.notification_service.add_notification(
                    blog_address_names = await self.comment_store.get_replies_blog_address_name(user_blog.address_name, parent_id),
                    username=user.username,
                    type=4,
                    notification_blog_name=blog.blog_name,
                    notification_blog_image_url=user_blog.main_image_url,
                    comment_id=new_comment.id
                )
            return CommentDetailResponse.from_comment(new_comment, user)

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
    

    # 페이지네이션 정보를 추가로 내려주고 싶으면
    async def get_guestbook_list_pagination(
        self,
        blog_id: int,
        page: int,
        per_page: int,
        current_user: Optional[User] = None  # ← 추가
    ) -> PaginatedCommentListResponse:
        total_count = await self.comment_store.get_guestbook_comments_count(blog_id)
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