
from wastory.app.hometopic.models import Hometopic
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION

class HometopicStore:

    @transactional
    async def create_hometopic(
        self, topicname:str,high_category:int
        )->Hometopic:
            hometopic=Hometopic(
                name=topicname,
                high_categry=high_category
            )
            SESSION.add(hometopic)
            await SESSION.flush()
            await SESSION.refresh(hometopic)
            return hometopic
    