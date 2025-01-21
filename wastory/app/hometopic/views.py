from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,HTTP_204_NO_CONTENT


from wastory.app.user.models import User
hometopic_router = APIRouter()
from wastory.app.user.views import login_with_header
from wastory.app.hometopic.dto.requests import HometopicCreateRequest
from wastory.app.hometopic.dto.responses import HometopicDetailResponse
from wastory.app.hometopic.service import HometopicService
#카테고리를 생성하는 API
@hometopic_router.post("/create", status_code=HTTP_201_CREATED)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    Hometopic_create_request:HometopicCreateRequest,
    Hometopic_service: Annotated[HometopicService, Depends()],
)-> HometopicDetailResponse:
    return await Hometopic_service.create_hometopic(
        topic_name=Hometopic_create_request.topicname
    )
