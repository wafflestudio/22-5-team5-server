from typing import Annotated

from fastapi import Depends
from wastory.app.category.dto.responses import CategoryDetailResponse,CategoryListResponse
from wastory.app.category.errors import BlogNotFoundError
from wastory.app.user.models import User
from wastory.app.blog.store import BlogStore
class GuestbookService:
    def __init__(
        self, 
        blog_store:Annotated[BlogStore,Depends()],
        guestbook_store:Annotated[GuestBook,Depends()])-> None:
        self.category_store = category_store
        self.user_store=user_store
        self.blog_store=blog_store
        self.guestbook_store=guestbook_store

    def create_guestbook(
        self, user:User
    )-> None:
        blog=await self.blog_store.get_blog_of_user(user)
        if blog==None:
            raise BlogNotFoundError()
        await self.guestbook_store.create_guestbook(
            blog_id=blog.id,
            blog_name=blog.blog_name
        )


    