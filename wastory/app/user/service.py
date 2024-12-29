from typing import Annotated

from fastapi import Depends
from wastory.app.user.models import User
from wastory.app.user.store import UserStore


class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()]) -> None:
        self.user_store = user_store

    def add_user(self, username: str, password: str, email: str):
        self.user_store.add_user(username=username, password=password, email=email)

    def get_user_by_username(self, username: str) -> User | None:
        return self.user_store.get_user_by_username(username)

    def update_user(
        self,
        username: str,
        email: str | None,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        return self.user_store.update_user(username, email, address, phone_number)