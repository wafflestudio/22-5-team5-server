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
    draft: ArticleCreateRequest,
    draft_service: Annotated[DraftService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
) -> DraftResponse:
    user_blog = await blog_service.get_blog_by_user(user)

    return await draft_service.create_draft(
        user=user, 
        draft_title=article.title, 
        draft_content=article.content
        )
    

# article 수정
@draft_router.patch("/update/{draft_id}", status_code=200)
async def update_draft(
    user: Annotated[User, Depends(login_with_header)],
    draft_id: int,
    blog_service: Annotated[BlogService, Depends()],
    draft_service: Annotated[DraftService, Depends()],
) -> DraftResponse:
    user_blog = await blog_service.get_blog_by_user(user)
    return await draft_service.update_article(
        user=user,
        draft_id = draft_id,
        draft_title=draft.title, 
        draft_content=draft.content
    )

# article 정보 가져오기
@draft_router.get("/get/{draft_id}", status_code=200)
async def get_draft_by_id(
    draft_service: Annotated[DraftService, Depends()],
    user: Annotated[User, Depends(login_with_header)],
    draft_id : int,
) -> DraftResponse :
    return await draft_service.get_draft_by_id(user, draft_id)



# blog 내 draft 목록 가져오기
@draft_router.get("/blogs/{blog_id}", status_code=200)
async def get_drafts_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    blog_id : int,
    page: int
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_in_blog(
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )

# draft 삭제
@draft_router.delete("/delete/{draft_id}", status_code=204)
async def delete_article(
    user: Annotated[User, Depends(login_with_header)],
    draft_id: int,
    article_service: Annotated[ArticleService, Depends()],
) -> None:
    await article_service.delete_article(user, article_id)