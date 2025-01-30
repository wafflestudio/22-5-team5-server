from pydantic import BaseModel
class PresignedUrlRequest(BaseModel):
    file_name: str
    file_type: str
    
class ImageCreateRequest(BaseModel):
    file_url: str 