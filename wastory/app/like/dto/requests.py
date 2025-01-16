from pydantic import BaseModel

class LikeCreateRequest(BaseModel):
    article_id : int
