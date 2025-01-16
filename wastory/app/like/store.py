from functools import cache
from typing import Annotated, Sequence, Optional

from sqlalchemy import select, or_, and_
from wastory.app.like.errors import LikeNotFoundError
from wastory.app.like.models import Like
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION

class LikeStore :
    @transactional
    async def create_like(
        self, blog_id : int, article_id : int,
    ) -> Like :
        
        like = Like(
           blog_id = blog_id, article_id = article_id
        )
        SESSION.add(like)
        # 왜 필요하지?       
        await SESSION.flush()
        await SESSION.refresh(like)
        
        return like
    
    @transactional
    async def delete_like(self, like: Like) -> None:
        if like is None: 
            raise LikeNotFoundError()
        await SESSION.delete(like)
        await SESSION.flush()       

    @transactional
    async def get_like_by_id(self, like_id : int) -> Like | None:
        like = await SESSION.get(Like, like_id)
        return like
    
    # 특정 blog 가 누른 like 를 얻는 method
    @transactional
    async def get_likes_by_blog(self, blog_id: int) -> Sequence[Like]:
        query = select(Like).where(Like.blog_id == blog_id)
        result = await SESSION.scalars(query)  # await 추가
        return result.all()    

    # article 이 받은 like 조회
    @transactional
    async def get_likes_in_article(self, article_id: int) -> Sequence[Like]:
        query = select(Like).where(Like.article_id == article_id)
        result = await SESSION.scalars(query)  # await 추가
        return result.all()   
    
    
    @transactional
    async def get_like_by_blog_and_article(self, blog_id: int, article_id: int) -> Optional[Like]:
        result = await SESSION.execute(
            select(Like).where(Like.blog_id == blog_id, Like.article_id == article_id)
        )
        row = result.one_or_none()
        return row[0] if row else None  # 스칼라 값을 반환


    # blog 가 article 에 좋아요를 눌렀는지 확인하기.
    @transactional
    async def blog_press_like(self, blog_id: int, article_id: int) -> bool:
        """
        특정 blog가 특정 article에 대해 좋아요를 눌렀는지 여부를 확인합니다.
        """
        query = select(Like).where(
            (Like.blog_id == blog_id) & (Like.article_id == article_id)
        )
        result = await SESSION.scalars(query)
        like = result.first()

        return like is not None
