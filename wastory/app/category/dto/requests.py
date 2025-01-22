from typing import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator,model_validator

from wastory.app.category.errors import InvalidFieldFormatError



def validate_categoryname(value:str)->str:
    if(len(value)>50):
        raise InvalidFieldFormatError()
    return value

def validate_categorylevel(value:int)->int:
    if value < 0 or value > 2:
        raise InvalidFieldFormatError()
    return value

class CategoryCreateRequest(BaseModel):
    categoryname: Annotated[str,AfterValidator(validate_categoryname)]
    categoryLevel: Annotated[int, AfterValidator(validate_categorylevel)]
    parent_id: int|None=None

    @model_validator(mode="after")
    def validate_level_and_parent_id(self) -> "CategoryCreateRequest":
        if self.categoryLevel not in (1, 2):  # level 값이 1 또는 2가 아닐 경우 에러 처리
            raise InvalidFieldFormatError()
        if self.categoryLevel == 2 and self.parent_id is None:
            raise InvalidFieldFormatError()
        if self.categoryLevel == 1 and self.parent_id is not None:
            raise InvalidFieldFormatError()
        return self

class CategoryUpdateRequest(BaseModel):
    categoryname: Annotated[str,AfterValidator(validate_categoryname)]

