from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, field_validator, Field

from wastory.common.errors import InvalidFieldFormatError

    
class NotificationDeleteRequest(BaseModel):
    notification_id: int|None = None

class NotificationCheckRequest(BaseModel):
    notification_id: int|None = None