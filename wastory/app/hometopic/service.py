from typing import Annotated

from fastapi import Depends
from wastory.app.hometopic.store import HometopicStore
from wastory.app.hometopic.dto.responses import HometopicDetailResponse
class HometopicService:
    def __init__(
        self, 
        hometopic_store: Annotated[HometopicStore, Depends()])->None:
        self.hometopic_store=hometopic_store


    async def create_hometopic(
        self, topic_name:str, high_category:int
        )-> HometopicDetailResponse:
            
            new_topic= await self.hometopic_store.create_hometopic(
                topicname=topic_name,
                high_category=high_category
            )
            return HometopicDetailResponse.from_hometopic(new_topic)
   