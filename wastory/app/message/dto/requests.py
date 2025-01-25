from pydantic import BaseModel


class MessageCreateRequest(BaseModel):
    recipient_user_id: int  
    content: str  


class MessageUpdateRequest(BaseModel):
    content: str  