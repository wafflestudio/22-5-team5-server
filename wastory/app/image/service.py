from typing import Annotated
from fastapi import File, UploadFile, Depends, HTTPException

from wastory.app.image.dto.responses import ImageDetailResponse
from wastory.app.image.store import ImageStore
from wastory.app.image.errors import S3ClientError, UnexpectedError
from botocore.exceptions import ClientError

class ImageService:
    def __init__(
        self,
        image_store: Annotated[ImageStore, Depends()]
    ) : 
        self.image_store = image_store
    
    async def upload_image(
        self,
        s3_path : str,
        file: UploadFile = File(...)
    ) -> ImageDetailResponse :
        try:
            file_url = await self.image_store.upload_image(s3_path, file)
            return ImageDetailResponse.from_image(file_url)
        except ClientError as e:
            raise S3ClientError
        except Exception as e:
            raise UnexpectedError
        
    async def delete_image(
        self,
        file_url : str
    ) -> dict :
        try:
            return await self.image_store.delete_image(file_url)
        except ClientError as e:
            raise S3ClientError
        except Exception as e:
            raise UnexpectedError
        