from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, field_validator, Field

from wastory.common.errors import InvalidFieldFormatError


class NotificationCreateRequest(BaseModel):
    address_name: str

    @field_validator("address_name")
    def validate_address_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if len(value) < 3 or len(value) > 20:
            raise InvalidFieldFormatError()
        if " " in value:
            raise InvalidFieldFormatError()
        return value
    
class NotificationDeleteRequest(BaseModel):
    notification_id: int|None = None

class NotificationCheckRequest(BaseModel):
    notification_id: int|None = None