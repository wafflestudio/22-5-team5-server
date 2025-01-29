from typing import Annotated, Optional
from pydantic import BaseModel, ValidationError, model_validator,AfterValidator

from wastory.app.comment.errors import InvalidFieldFormatError

# Validator for content length
def content_max_length_5000(content: str | None) -> str | None:
    if content is None:
        return None  # None is allowed
    if len(content) > 5000:
        raise InvalidFieldFormatError("내용은 5000자를 초과할 수 없습니다.")
    return content

class CommentCreateRequest(BaseModel):
    content: Annotated[
        str,
        AfterValidator(content_max_length_5000),
    ]
    parent_id: Optional[int] = None
    secret: int  # 0 또는 1로 표현된 값이라고 가정
    level: int

    @model_validator(mode="after")
    def validate_level_and_parent_id(self) -> "CommentCreateRequest":
        if self.level not in (1, 2):  # level 값이 1 또는 2가 아닐 경우 에러 처리
            raise InvalidFieldFormatError()
        if self.level == 2 and self.parent_id is None:
            raise InvalidFieldFormatError()
        if self.level == 1 and self.parent_id is not None:
            raise InvalidFieldFormatError()
        return self

    
    
class CommentUpdateRequest(BaseModel):
    content: Annotated[
        str,
        AfterValidator(content_max_length_5000),
    ]
    secret:Optional[int] = None