from sqlalchemy import select
from wastory.database.connection import SESSION
from wastory.database.annotation import transactional
from wastory.app.guestbook.models import GuestBook

class GuestBookStore:
    async def get_guestbook_by_id(self, guestbook_id: int) -> GuestBook | None:
        stmt = select(GuestBook).filter(GuestBook.id == guestbook_id)
        result = await SESSION.scalar(stmt)
        return result

    @transactional
    async def create_guestbook(self, blog_id:int,blog_name:str) -> GuestBook:
        guestbook = GuestBook(
            blog_name=blog_name,
            blog_id=blog_id,
            )
        SESSION.add(guestbook)
        await SESSION.flush()
        await SESSION.refresh(guestbook)
        return guestbook

    # 필요하다면 update, delete 등 추가