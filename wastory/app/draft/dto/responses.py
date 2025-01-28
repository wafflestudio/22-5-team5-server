from fastapi import Depends
from typing import Self, Annotated
from pydantic import BaseModel
from datetime import datetime
from wastory.app.draft.models import Draft

class DraftResponse(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime

    @staticmethod
    def from_draft(draft:Draft | None) -> "DraftResponse":
        
        return DraftResponse(
            id=draft.id, 
            title=draft.title, 
            content=draft.content,
            created_at=draft.created_at
        )

class DraftResponseForList(BaseModel):
    id:int
    title:str
    created_at:datetime
    @staticmethod
    def from_draft(draft:Draft | None) -> "DraftResponseForList":
        
        return DraftResponseForList(
            id=draft.id, 
            title=draft.title, 
            created_at=draft.created_at
        )


class DraftListResponse(BaseModel):
    page:int
    per_page:int
    total_count:int
    drafts:list[DraftResponseForList]
