from typing import Annotated

from fastapi import Depends
from wastory.app.blog.models import Blog
from wastory.app.user.models import User
from wastory.app.blog.store import BlogStore


class UserService:
    def __init__(self, blog_store: Annotated[BlogStore, Depends()]) -> None:
        self.blog_store = blog_store

    async def create_blog(
        self,
        user : User,
        name : str,
        description : str
    ) -> 

    async def add_user(self, username: str, password: str, email: str):
        await self.blog_store.add_blog(username=username, password=password, email=email)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_store.get_user_by_username(username)

    async def update_user(
        self,
        username: str,
        email: str | None,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        return await self.user_store.update_user(username, email, address, phone_number)