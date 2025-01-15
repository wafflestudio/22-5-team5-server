from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED,HTTP_204_NO_CONTENT

from wastory.app.user.models import User
comment_router = APIRouter()
from wastory.app.user.views import login_with_header
from wastory.app.comment.service import CommentService
from wastory.app.comment.dto.requests import CommentCreateRequest, CommentUpdateRequest
from wastory.app.comment.dto.responses import CommentDetailResponse,CommentListResponse

@comment_router.post("/article/{article_id}", status_code=HTTP_201_CREATED)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    comment_service: Annotated[CommentService, Depends()],
    comment_request: CommentCreateRequest,
    article_id:int,
)-> CommentDetailResponse:
    return await comment_service.create_comment(
        content=comment_request.content,
        level=comment_request.level,
        secret=comment_request.secret,
        user=user,
        article_id=article_id,
        parent_id=comment_request.parent_id
    )

@comment_router.patch("/{comment_id}", status_code=HTTP_200_OK)
async def update(
    user:Annotated[User,Depends(login_with_header)],
    comment_id:int,
    comment_service: Annotated[CommentService,Depends()],
    comment_request: CommentUpdateRequest
)-> CommentDetailResponse:
    return await comment_service.update_comment(
        user=user, 
        comment_id=comment_id,
        content=comment_request.content
    )

@comment_router.delete("/{comment_id}", status_code=HTTP_204_NO_CONTENT)
async def delete(
    user:Annotated[User,Depends(login_with_header)],
    comment_service: Annotated[CommentService,Depends()],
    comment_id:int,
)-> None:
    await comment_service.delete_comment(
        user=user,
        comment_id=comment_id
    )

#이거는 일단은 그냥 user 체크 안하고 모든걸 다 리스트화해서 보냄
#(유저별로 비밀 안 비밀 표시 어케할지 고만해야 할듯..)
@comment_router.get("/article/{article_id}/{page}", status_code=HTTP_200_OK)
async def get_comment_list(
    article_id: int,
    page: int,
    comment_service: Annotated[CommentService, Depends()],
) -> list[CommentListResponse]:
    per_page = 10  # 페이지당 10개(혹은 쿼리 파라미터로 받아도 됨)
    return await comment_service.get_list_level1_with_children(
        article_id=article_id,
        page=page,
        per_page=per_page
    )


