from pydantic import BaseModel, Field
from datetime import datetime


class BlogDetailResponse(BaseModel):
    id: int
    blog_name: str = Field(serialization_alias="blog_name")
    description : str
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True  # SQLAlchemy 모델에서 데이터를 가져올 때 Pydantic 변환 지원