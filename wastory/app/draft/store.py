from functools import cache
from typing import Annotated, Sequence
from datetime import datetime, timedelta
from sqlalchemy import select, or_, and_, func, update
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.elements import ClauseElement

from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.user.models import User
from wastory.app.draft.models import Draft

class DraftStore :
    @transactional
    async def create_article(
        self, 
        draft_title : str, 
        draft_content: str, 
        blog_id:int
    ) -> Draft :
        draft = Draft(
            title = draft_title, 
            content = draft_content, 
            blog_id=blog_id
        )
        SESSION.add(draft)
        # 왜 필요하지?       
        await SESSION.flush()
        await SESSION.refresh(draft)
        return draft
    
    @transactional
    async def update_article(
        self,
        draft:Draft,
        draft_title : str, 
        draft_content: str, 
    ) -> Draft:
        if draft_title is not None:
            draft.title = draft_title
        if draft_content is not None:
            draft.content = draft_content

        await SESSION.merge(draft)
        await SESSION.flush()
        return draft
    

    @transactional
    async def delete_article(self, draft: Draft) -> None:
        await SESSION.delete(draft)
        await SESSION.flush()   


    @transactional
    async def get_draft_by_id(self, draft_id: int) -> Article | None:
        stmt = select(Draft).filter(Draft.id==draft_id)
        draft = await SESSION.execute(stmt)
        return draft

    @transactional
    async def get_drafts_by_blog_id(self, blog_id: int) -> Article | None:
        stmt = select(Draft).filter(Draft.blog_id==blog_id)
        drafts = await SESSION.execute(stmt)
        return drafts
