from typing import Self
from pydantic import BaseModel

from wastory.app.user.models import User


class MyProfileResponse(BaseModel):
    username: str
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