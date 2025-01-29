from typing import Annotated
from pydantic import AfterValidator, BaseModel,model_validator
from fastapi import HTTPException

class InvalidFieldFormatError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

def title_length_1_and_80(title: str | None) -> str | None:
    if title.strip() is "":
        return ""  # None은 허용
    if len(title) < 1 or len(title) > 80:
        raise InvalidFieldFormatError("제목은 2자 이상 80자 이하로 작성해야 합니다.")
    return title


def content_min_valid_character(content: str | None) -> str | None:
    if content.strip() is "":
        return ""  # None은 허용
    if len(content.strip()) == 0:
        raise InvalidFieldFormatError("내용에는 최소 1개의 문자(공백 제외)가 포함되어야 합니다.")
    return content


class DraftCreateRequest(BaseModel):
    title: Annotated[
        str | None,
        AfterValidator(title_length_1_and_80)
    ]
    content: Annotated[
        str | None,
        AfterValidator(content_min_valid_character)
    ]

    @model_validator(mode="after")
    def validate_title_and_content(cls, values):
        title = values.title
        content = values.content
        
        # 제목과 내용이 둘 다 비어 있을 때 에러 발생
        if (title is None or title.strip() == "") and (content is None or content.strip() == ""):
            raise InvalidFieldFormatError("제목과 내용 중 하나는 반드시 입력해야 합니다.")
        
        return values


class DraftUpdateRequest(BaseModel):
    title: Annotated[
        str | None,
        AfterValidator(title_length_1_and_80)
    ] = None
    content: Annotated[
        str | None,
        AfterValidator(content_min_valid_character)
    ] = None
