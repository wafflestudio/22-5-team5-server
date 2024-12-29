from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wastory.app.user.errors import EmailAlreadyExistsError, UserUnsignedError, UsernameAlreadyExistsError
from wastory.app.user.models import User
from wastory.database.connection import get_db_session


class UserStore:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def add_user(self, username: str, password: str, email: str) -> User:
        if self.get_user_by_username(username):
            raise UsernameAlreadyExistsError()

        if self.get_user_by_email(email):
            raise EmailAlreadyExistsError()

        user = User(username=username, password=password, email=email)
        self.session.add(user)
        return user

    def get_user_by_username(self, username: str) -> User | None:
        return self.session.scalar(select(User).where(User.username == username))

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))

    def update_user(
        self,
        username: str,
        email: str | None,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        user = self.get_user_by_username(username)
        if user is None:
            raise UserUnsignedError()

        if email is not None:
            if self.get_user_by_email(email):
                raise EmailAlreadyExistsError()
            user.email = email

        if address is not None:
            user.address = address

        if phone_number is not None:
            user.phone_number = phone_number

        return user