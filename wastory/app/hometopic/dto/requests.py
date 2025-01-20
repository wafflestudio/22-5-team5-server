from typing import Annotated
from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator

from wastory.app.hometopic.errors import InvalidFieldFormatError



def validate_topicname(value:str)->str:
    if(len(value)>50):
        raise InvalidFieldFormatError()
    return value


class HometopicCreateRequest(BaseModel):
    topicname: Annotated[str,AfterValidator(validate_topicname)]

class HometopicUpdateRequest(BaseModel):
    topicname: Annotated[str,AfterValidator(validate_topicname)]

