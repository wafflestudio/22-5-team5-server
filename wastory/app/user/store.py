from datetime import datetime
from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wastory.app.user.errors import EmailAlreadyExistsError, UserUnsignedError, UsernameAlreadyExistsError, InvalidUsernameOrPasswordError
from wastory.app.user.models import User, BlockedToken
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION

class UserStore:
    @transactional
    async def add_user(self, email: str, password: str) -> User:
        if await self.get_user_by_email(email):
            raise EmailAlreadyExistsError()
        user = User(password=password, email=email)
        SESSION.add(user)
        return user

    async def get_user_by_id(self, id: int) -> User | None:
        return await SESSION.scalar(select(User).where(User.id == id))

    async def get_user_by_username(self, username: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.username == username))

    async def get_user_by_nickname(self, nickname: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.nickname == nickname))

    async def get_user_by_email(self, email: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.email == email))

    @transactional
    async def update_user(
        self,
        user : User,
        username: str | None,
        nickname: str | None,
    ) -> User:
        if username is not None:
            user.username = username

        if nickname is not None:
            user.nickname = nickname

        return user


    @transactional
    async def update_username(self, username:str, email:str) -> User:
        user = await self.get_user_by_email(email)
        if user is None:
            raise UserUnsignedError()
        if username is not None:
            user.username = username


    @transactional
    async def update_password(self, email:str, old_password: str, new_password: str) -> User:
        user = await self.get_user_by_email(email)
        if user is None:
            raise UserUnsignedError()

        if user.password != old_password:
            raise InvalidUsernameOrPasswordError()


    @transactional
    async def delete_user(self, user_id: int) -> User | None:
        deleted_user = await SESSION.scalar(select(User).where(User.id == user_id))
        await SESSION.delete(deleted_user)  
        await SESSION.flush()
        return deleted_user
        

    @transactional
    async def block_token(self, token_id: str, expired_at: datetime) -> None:
        blocked_token = BlockedToken(token_id=token_id, expired_at=expired_at)
        SESSION.add(blocked_token)

    async def is_token_blocked(self, token_id: str) -> bool:
        return (
            await SESSION.scalar(
                select(BlockedToken).where(BlockedToken.token_id == token_id)
            )
            is not None
        )