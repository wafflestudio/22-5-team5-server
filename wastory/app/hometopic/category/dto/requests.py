from typing import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

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

class CategoryUpdateRequest(BaseModel):
    categoryname: Annotated[str,AfterValidator(validate_categoryname)]

