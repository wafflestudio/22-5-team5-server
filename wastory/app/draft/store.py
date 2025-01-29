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
from wastory.app.blog.models import Blog
from wastory.app.draft.dto.responses import DraftResponse,DraftListResponse,DraftResponseForList

class DraftStore :
    @transactional
    async def create_draft(
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
    async def update_draft(
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
    async def get_draft_by_id(self, draft_id: int) -> Draft | None:
        stmt = select(Draft).filter(Draft.id==draft_id)
        draft = await SESSION.scalar(stmt)
        return draft

    
    

    @transactional
    async def get_drafts_in_blog(self, blog_id: int, page: int, per_page: int) -> DraftListResponse:
        offset_val = (page - 1) * per_page

        # 쿼리 작성: Article에 likes와 comments를 조인하여 계산
        stmt = (
            select(
                Draft
            )
            .join(Blog, Blog.id == Draft.blog_id)
            .filter(Draft.blog_id == blog_id)
            .order_by(Draft.created_at.desc())
            .offset(offset_val)
            .limit(per_page)
        )

        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환하여 필요한 데이터만 반환
        drafts = [
            DraftResponseForList.from_draft(
                draft=row.Draft
            )
            for row in rows
        ]

        # 전체 개수 계산
        total_count_stmt = select(func.count(Draft.id)).filter(Draft.blog_id == blog_id)
        total_count = await SESSION.scalar(total_count_stmt)

        return DraftListResponse(
            total_count=total_count or 0,
            page=page,
            per_page=per_page,
            drafts=drafts,
        )

    @transactional
    async def delete_draft(self, draft: Draft) -> None:
        await SESSION.delete(draft)
        await SESSION.flush()  
