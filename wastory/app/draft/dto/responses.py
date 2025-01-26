from fastapi import Depends
from typing import Self, Annotated
from pydantic import BaseModel
from datetime import datetime

class DraftResponse(BaseModel):
    id:int
    title:str
    created_at:datetime

    @staticmethod
    def from_draft(article: Article | None) -> "DraftResponse":
        
        return DraftResponse(
            id=article.id, 
            title=article.title, 
            created_at=article.created_at
        )


class DraftListResponse(BaseModel):
    total_count:int
    drafts:list[DraftResponse]