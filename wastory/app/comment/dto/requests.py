from typing import Annotated, Optional
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

from wastory.app.comment.errors import InvalidFieldFormatError

def content_max_length_5000(content: str | None) -> str | None:
    if content is None:
        return None  # None은 허용
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
    level:int

class CommentUpdateRequest(BaseModel):
    content: Annotated[
        str,
        AfterValidator(content_max_length_5000),
    ]