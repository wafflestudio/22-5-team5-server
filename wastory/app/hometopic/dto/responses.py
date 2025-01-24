from pydantic import BaseModel
from typing import List, Optional

from wastory.app.hometopic.models import Hometopic



class HometopicDetailResponse(BaseModel):
    id: int
    hometopic_name: str

    @staticmethod
    def from_hometopic(hometopic:Hometopic) -> "HometopicDetailResponse":
        response = HometopicDetailResponse(
            id=hometopic.id,
            hometopic_name=hometopic.name
        )

        return response
    

class HometopicListResponse(BaseModel):
    id: int
    name: str
    high_category : int

    # 설정 추가
    model_config = {
        "from_attributes": True
    }

    @staticmethod
    def from_hometopic(hometopic: Hometopic) -> "HometopicListResponse":
        return HometopicListResponse(
            id = hometopic.id,
            name = hometopic.name,
            high_category = hometopic.high_category
        )

class PaginatedHometopicListResponse(BaseModel):
    hometopics: list[HometopicListResponse]


