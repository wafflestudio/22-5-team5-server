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

