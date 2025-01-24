from pydantic import BaseModel

from wastory.app.user.models import User


class MyProfileResponse(BaseModel):
    username: str | None
    email: str
    is_kakao_user: bool

    @staticmethod
    def from_user(user: User) -> "MyProfileResponse":
        return MyProfileResponse(
            username=user.username,
            email=user.email,
            is_kakao_user=user.nickname is not None
        )


class UserSigninResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserVerifyResponse(BaseModel):
    verification: bool

class EmailVerifyResponse(BaseModel):
    verification: bool