from typing import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

from wastory.app.category.errors import InvalidFieldFormatError



def validate_categoryname(value:str)->str:
    if(len(value)>50):
        raise InvalidFieldFormatError()

def validate_categorylevel(value:int)->int:
    if value < 0 or value > 2:
        raise InvalidFieldFormatError()

class CategoryCreateRequest(BaseModel):
    categoryname: Annotated[str,AfterValidator(validate_categoryname)]
    categoryLevel: Annotated[int, AfterValidator(validate_categorylevel)]
    parentId: int|None=None

class CategoryUpdateRequest(BaseModel):
    categoryname: Annotated[str,AfterValidator(validate_categoryname)]

