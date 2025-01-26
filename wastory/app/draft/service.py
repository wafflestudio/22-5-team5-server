from typing import Annotated

from fastapi import Depends
from wastory.app.draft.dto.responses import DraftListResponse,DraftResponse 
from wastory.app.draft.errors import DraftNotFoundError, NoAuthoriztionError
from wastory.app.blog.errors import BlogNotFoundError
from wastory.app.blog.store import BlogStore
from wastory.app.draft.store import DraftStore
from wastory.app.user.errors import PermissionDeniedError
from wastory.app.user.models import User 

class DraftService:
    def __init__(
        self,
        blog_store: Annotated[BlogStore, Depends()],
        draft_store:Annotated[DraftStore,Depends()]
    ):
        self.blog_store = blog_store
        self.draft_store= draft_store
    
    async def create_draft(
        self, 
        user: User, 
        draft_title: str, 
        draft_content: str, 
    ) -> DraftResponse :
                
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
    
        new_draft = await self.draft_store.create_draft(
            draft_title=article_title, 
            draft_content=article_content, 
            blog_id=user_blog.id, 
        )
        
        return DraftResponse.from_draft(new_draft)
    
    async def update_draft(
        self, 
        user: User,
        draft_id: int,
        draft_title: str,
        draft_content: str,
    ) -> DraftResponse:
        
        # 사용자의 Blog 확인
        user_blog = await self.blog_store.get_blog_of_user(user.id)
        if user_blog is None:
            raise BlogNotFoundError()
        
        draft = await self.draft_store.get_draft_by_id(draft_id)
        if draft is None: 
            raise DraftNotFoundError()
        
        # 권한 검증
        if draft.blog_id != user_blog.id:
            raise PermissionDeniedError()
    
        
        updated_draft = await self.draft_store.update_draft(
            draft,
            draft_title, 
            draft_content
            )

        return DraftResponse.from_draft(updated_draft)

    