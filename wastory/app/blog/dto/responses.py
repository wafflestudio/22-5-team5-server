from pydantic import BaseModel, Field
from sqlalchemy import DateTime


class BlogDetailResponse(BaseModel):
    id: int
    name: str = Field(serialization_alias="blog_name")
    description : str
    created_at : DateTime
    updated_at : DateTime