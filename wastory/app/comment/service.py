from typing import Annotated

from fastapi import Depends
from wastory.app.comment.store import CommentStore
from wastory.app.comment.dto.responses import CommentDetailResponse
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.user.models import User
from wastory.app.user.store import UserStore
from wastory.app.article.store import ArticleStore
class CommentService:
    def __init__(
        self, 
        comment_store: Annotated[CommentStore, Depends()],
        user_store:Annotated[UserStore,Depends()],
        article_store:Annotated[ArticleStore,Depends()]) -> None:
        self.comment_store = comment_store
        self.user_store=user_store
        self.article_store=article_store


    async def create_comment(
        self, content:str,level:int,secret:int,user:User,article_id:int,parent_id:int
        )-> CommentDetailResponse:
            #article id를 받아서, article 을 받고 넘기자
            article=self.article_store.get_article_by_id(article_id=article_id)
            if article==None:
                raise ArticleNotFoundError()
            if level==1:
                new_comment=await self.comment_store.create_comment_1(
                    content=content,
                    secret=secret,
                    user=user,
                    article=article,
                    article_id=article_id
                )
            elif level==2:
                new_comment=await self.comment_store.create_comment_2(
                    content=content,
                    secret=secret,
                    user=user,
                    article=article,
                    article_id=article_id,
                    parent_id=parent_id
                )
            return CommentDetailResponse.from_comment(new_comment)

    