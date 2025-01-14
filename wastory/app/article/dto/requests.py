from typing import Annotated
from pydantic import AfterValidator, BaseModel

from wastory.common.errors import InvalidFieldFormatError


def title_length_2_and_100(title: str | None) -> str | None:
    if title is None:
        return None  # None은 허용
    if len(title) < 2 or len(title) > 100:
        raise InvalidFieldFormatError("제목은 2자 이상 100자 이하로 작성해야 합니다.")
    return title


def title_not_empty(title: str | None) -> str | None:
    if title is None:
        return None  # None은 허용
    if title.strip() == "":
        raise InvalidFieldFormatError("제목은 공백만으로 구성될 수 없습니다.")
    return title

def content_min_valid_character(content: str | None) -> str | None:
    if content is None:
        return None  # None은 허용
    if len(content.strip()) == 0:
        raise InvalidFieldFormatError("내용에는 최소 1개의 문자(공백 제외)가 포함되어야 합니다.")
    return content


def content_max_length_5000(content: str | None) -> str | None:
    if content is None:
        return None  # None은 허용
    if len(content) > 5000:
        raise InvalidFieldFormatError("내용은 5000자를 초과할 수 없습니다.")
    return content


class ArticleCreateRequest(BaseModel):
    title: Annotated[
        str,
        AfterValidator(title_length_2_and_100),
        AfterValidator(title_not_empty),
    ]
    content: Annotated[
        str,
        AfterValidator(content_min_valid_character),
        AfterValidator(content_max_length_5000),
    ]
    category_id : int


class ArticleUpdateRequest(BaseModel):
    title: Annotated[
        str | None,
        AfterValidator(title_length_2_and_100),
        AfterValidator(title_not_empty),
    ] = None
    content: Annotated[
        str | None,
        AfterValidator(content_min_valid_character),
        AfterValidator(content_max_length_5000),
    ] = None
