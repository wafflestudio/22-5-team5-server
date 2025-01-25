from typing import Annotated
from fastapi import APIRouter, Depends


from wastory.app.user.models import User
from wastory.app.user.views import login_with_header
from wastory.app.hometopic.dto.requests import HometopicCreateRequest
from wastory.app.hometopic.dto.responses import HometopicDetailResponse, PaginatedHometopicListResponse
from wastory.app.hometopic.service import HometopicService
#카테고리를 생성하는 API

hometopic_router = APIRouter()

@hometopic_router.post("/create", status_code=201)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    hometopic_create_request:HometopicCreateRequest,
    hometopic_service: Annotated[HometopicService, Depends()],
)-> HometopicDetailResponse:
    return await hometopic_service.create_hometopic(
        topic_name=hometopic_create_request.topicname,
        high_category=hometopic_create_request.high_category
    )

@hometopic_router.get("/list", status_code = 200)
async def get_hometopic_list(
    hometopic_service: Annotated[HometopicService, Depends()]
) -> PaginatedHometopicListResponse :
    return await hometopic_service.get_hometopic_list()
