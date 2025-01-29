from typing import Annotated
from fastapi import APIRouter, Depends
from wastory.app.draft.dto.requests import DraftCreateRequest, DraftUpdateRequest
from wastory.app.draft.dto.responses import DraftListResponse,DraftResponse
from wastory.app.draft.service import DraftService
from wastory.app.blog.service import BlogService

from wastory.app.user.models import User
from wastory.app.user.views import login_with_header


draft_router = APIRouter()

# draft 생성
@draft_router.post("/create", status_code=201)
async def create_draft(
    user: Annotated[User, Depends(login_with_header)],
    draft: DraftCreateRequest,
    draft_service: Annotated[DraftService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
) -> DraftResponse:
    user_blog = await blog_service.get_blog_by_user(user)

    return await draft_service.create_draft(
        user=user, 
        draft_title=draft.title, 
        draft_content=draft.content
        )
    

# article 수정
@draft_router.patch("/update/{draft_id}", status_code=200)
async def update_draft(
    user: Annotated[User, Depends(login_with_header)],
    draft_id: int,
    draft: DraftUpdateRequest,
    blog_service: Annotated[BlogService, Depends()],
    draft_service: Annotated[DraftService, Depends()],
) -> DraftResponse:
    user_blog = await blog_service.get_blog_by_user(user)
    return await draft_service.update_draft(
        user=user,
        draft_id = draft_id,
        draft_title=draft.title, 
        draft_content=draft.content
    )

# draft 정보 가져오기
@draft_router.get("/get/{draft_id}", status_code=200)
async def get_draft_by_id(
    draft_service: Annotated[DraftService, Depends()],
    user: Annotated[User, Depends(login_with_header)],
    draft_id : int
) -> DraftResponse :
    return await draft_service.get_draft_by_id(user, draft_id)



# blog 내 draft 목록 가져오기
@draft_router.get("/blogs/{blog_id}/{page}", status_code=200)
async def get_drafts_in_blog(
    draft_service: Annotated[DraftService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    blog_id : int,
    page: int
) -> DraftListResponse:
    per_page = 10
    return await draft_service.get_drafts_in_blog(
        page = page,
        per_page = per_page,
        user=user
    )

# draft 삭제
@draft_router.delete("/delete/{draft_id}", status_code=204)
async def delete_article(
    user: Annotated[User, Depends(login_with_header)],
    draft_id: int,
    draft_service: Annotated[DraftService, Depends()],
) -> None:
    await draft_service.delete_draft(user, draft_id)