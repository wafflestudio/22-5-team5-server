from typing import Self
from pydantic import BaseModel


class ImageDetailResponse(BaseModel):
    file_url : str

    @staticmethod
    def from_image(file_url: str) -> "ImageDetailResponse":
        return ImageDetailResponse(
            file_url=file_url
        )
    
class ImageDeleteResponse(BaseModel):
    file_url : str

    @staticmethod
    def from_image(file_url: str) -> "ImageDeleteResponse":
        return ImageDeleteResponse(
            file_url=file_url
        )