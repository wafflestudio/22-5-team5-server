from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, field_validator, Field

from wastory.common.errors import InvalidFieldFormatError


class BlogCreateRequest(BaseModel):
    blog_name: str
    description: str | None = None

    @field_validator("blog_name")
    def validate_store_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if len(value) < 3 or len(value) > 20:
            raise InvalidFieldFormatError()
        return value
    
class BlogUpdateRequest(BaseModel):
    blog_name: str|None = None
    description: str|None = None
