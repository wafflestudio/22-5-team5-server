from datetime import datetime, timedelta
from uuid import uuid4
from typing import Annotated, Optional
from enum import Enum

from fastapi import Depends
from wastory.database.settings import PW_SETTINGS
from wastory.app.user.errors import (
    InvalidUsernameOrPasswordError,
    InvalidTokenError,
    ExpiredSignatureError,
    BlockedTokenError,
)
from wastory.app.user.models import User
from wastory.app.user.store import UserStore
import jwt
import random
import smtplib
import redis
from email.message import EmailMessage


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()]) -> None:
        self.user_store = user_store

    async def add_user(self, email: str, password: str):
        await self.user_store.add_user(email=email, password=password)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_store.get_user_by_username(username)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_store.get_user_by_email(email)

    async def get_user_by_nickname(self, nickname: str) -> User | None:
        return await self.user_store.get_user_by_nickname(nickname)

    async def update_user(
        self,
        username: str | None,
        nickname: str | None,
        email: str,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        return await self.user_store.update_user(username, nickname, email, address, phone_number)

    async def update_password(
        self,
        email: str,
        old_password: str,
        new_password: str,
    ) -> User:
        return await self.user_store.update_password(email, old_password, new_password)

    async def update_username(
        self,
        username: str,
        email: str,
    ) -> User:
        return await self.user_store.update_username(username, email)

    async def signin(self, email: str, password: str) -> tuple[str, str]:
        user = await self.get_user_by_email(email)
        if user is None or user.password != password:
            raise InvalidUsernameOrPasswordError()
        return self.issue_tokens(user.email)
    
    def issue_tokens(self, email: str) -> tuple[str, str]:
        access_payload = {
            "sub": email,
            "exp": datetime.now() + timedelta(minutes=10),
            "typ": TokenType.ACCESS.value,
        }
        access_token = jwt.encode(access_payload, PW_SETTINGS.secret_for_jwt, algorithm="HS256")

        refresh_payload = {
            "sub": email,
            "jti": uuid4().hex,
            "exp": datetime.now() + timedelta(days=7),
            "typ": TokenType.REFRESH.value,
        }
        refresh_token = jwt.encode(refresh_payload, PW_SETTINGS.secret_for_jwt, algorithm="HS256")
        return access_token, refresh_token

    def validate_access_token(self, token: str) -> str:
        """
        access_token을 검증하고, username을 반환합니다.
        """
        try:
            payload = jwt.decode(
                token, PW_SETTINGS.secret_for_jwt, algorithms=["HS256"], options={"require": ["sub"]}
            )
            if payload["typ"] != TokenType.ACCESS.value:
                raise InvalidTokenError()
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def validate_refresh_token(self, token: str) -> str:
        """
        refresh_token을 검증하고, username을 반환합니다.
        """
        try:
            payload = jwt.decode(
                token,
                PW_SETTINGS.secret_for_jwt,
                algorithms=["HS256"],
                options={"require": ["sub"]},
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
        if payload["typ"] != TokenType.REFRESH.value:
            raise InvalidTokenError()
        # TODO 서비스의 규모가 커진다면 refresh_token을 검증하기 위해매번 DB를 조회하는 것은 비효율적입니다.
        # 그렇다면 어떻게 개선할 수 있을까요?
        # 답은 캐시를 이용하는 것입니다. 이 코드에는 구현되어 있지 않지만, 어떻게 사용하면 좋을지 고민해보세요.
        if await self.user_store.is_token_blocked(payload["jti"]):
            raise BlockedTokenError()
        return payload["sub"]


    async def reissue_tokens(self, refresh_token: str) -> tuple[str, str]:
        username = await self.validate_refresh_token(refresh_token)
        await self.user_store.block_token(refresh_token, datetime.now())
        return self.issue_tokens(username)


    def generate_verification_code(self) -> str:
        return str(random.randint(100000, 999999))


    async def send_verification_code(self, email: str) -> str:

        """무작위 인증 코드 생성 후 이메일 발송"""

        verification_code = self.generate_verification_code()

        # 캐시에 저장
        redis_client.set(f"verification:{email}", verification_code, ex=180) #3분

        # 이메일 발송
        msg = EmailMessage()
        msg["Subject"] = "Your Verification Code for Wastory"
        msg["From"] = "waffleteam05@gmail.com"
        msg["To"] = email
        msg.set_content(f"Your verification code is: {verification_code}")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("waffleteam05", PW_SETTINGS.gmail_app_password)
            server.send_message(msg)

        return verification_code

    def verify_code(self, email: str, code: str) -> bool:

        """Redis에서 인증 코드 검증"""

        stored_code: Optional[bytes] = redis_client.get(f"verification:{email}")
        if stored_code and stored_code.decode() == code:
            redis_client.delete(f"verification:{email}")  # 사용 후 삭제
            return True
        return False