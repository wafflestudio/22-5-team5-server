from pydantic import BaseModel

from wastory.app.user.models import User


class MyProfileResponse(BaseModel):
    username: str | None
    email: str
    address: str | None
    phone_number: str | None

    @staticmethod
    def from_user(user: User) -> "MyProfileResponse":
        return MyProfileResponse(
            username=user.username,
            email=user.email,
            address=user.address,
            phone_number=user.phone_number,
        )


class UserSigninResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserVerifyResponse(BaseModel):
    verification: bool

class EmailVerifyResponse(BaseModel):
    verification: bool