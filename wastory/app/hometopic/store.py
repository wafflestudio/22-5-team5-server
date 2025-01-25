from wastory.app.hometopic.models import Hometopic
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.hometopic.dto.responses import HometopicListResponse, PaginatedHometopicListResponse
from sqlalchemy import select

class HometopicStore:

    @transactional
    async def create_hometopic(
        self, topicname:str, high_category:int
        )->Hometopic:
            hometopic=Hometopic(
                name=topicname,
                high_categry=high_category
            )
            SESSION.add(hometopic)
            await SESSION.flush()
            await SESSION.refresh(hometopic)
            return hometopic
    
    @transactional
    async def get_hometopic_list(
        self,
        ) -> PaginatedHometopicListResponse :
        
        stmt = select(Hometopic)
        result = await SESSION.execute(stmt)
        rows = result.scalars().all()
        hometopics = [
            HometopicListResponse.from_hometopic(row) for row in rows
        ]
        
        return PaginatedHometopicListResponse(
            hometopics = hometopics
        )
    
    @transactional
    async def get_hometopic_id_list_by_high_hometopic_id(
        self,
        high_hometopic_id: int,
    ) -> list[int]:
        # Hometopic 데이터 쿼리
        stmt = (
            select(Hometopic.id)
            .filter(Hometopic.high_category == high_hometopic_id)
        )

        # 쿼리 실행
        result = await SESSION.execute(stmt)

        # 결과에서 ID 리스트 추출
        id_list = [row[0] for row in result.all()]

        return id_list
