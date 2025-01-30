import aioboto3
import uuid
from functools import cache
from typing import Annotated, Sequence
from fastapi import File, UploadFile

from sqlalchemy import select, or_, and_, func, update, event
from wastory.database.annotation import transactional
from wastory.database.settings import AWSSettings
from wastory.database.connection import SESSION

from wastory.app.image.dto.requests import PresignedUrlRequest
from wastory.app.image.errors import FileNotFoundError, UnexpectedError
from wastory.app.image.models import Image
from botocore.exceptions import ClientError

AWS_SETTINGS = AWSSettings()

async def delete_image_from_s3(target):
    """비동기적으로 S3에서 이미지 삭제"""
    await ImageStore().delete_image_in_S3(target.file_url)

def before_delete_image(mapper, connection, target):
    """Image 삭제 시 S3에서도 자동 삭제"""
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(delete_image_from_s3(target))
     # SQLAlchemy 이벤트 등록
    
event.listen(Image, "before_delete", before_delete_image)

class ImageStore:
    @transactional
    async def create_image(
        self,
        file_url: str,
        article_id: int | None = None,
        blog_id: int | None = None,
        is_main: bool = False 
    ) -> Image:
        image = Image(
            file_url=file_url,
            article_id=article_id,
            blog_id=blog_id,
            is_main=is_main 
        )
        SESSION.add(image)
        await SESSION.flush()
        await SESSION.refresh(image)
        return image 

    @transactional
    async def delete_image(self, image : Image) -> None:        
        await SESSION.delete(image)
        await SESSION.flush()
    
    @transactional
    async def get_image_of_article_by_url(self, article_id : int, file_url : str) -> Image:
        get_image_query = select(Image).filter(Image.article_id == article_id, Image.file_url == file_url)
        image = await SESSION.scalar(get_image_query)
        return image

    @transactional
    async def get_main_image_of_blog(self, blog_id : int) -> Image:
        get_image_query = select(Image).filter(Image.blog_id == blog_id, Image.is_main == True)
        image = await SESSION.scalar(get_image_query)
        return image


    async def upload_image_in_S3(
        self, 
        s3_path : str,
        file: UploadFile = File(...)
    ) -> str : 
        # S3 는 별도의 session 을 이용해야 한다고 합니다.
        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region
        ) as s3_client:
            await s3_client.upload_fileobj(
                file.file,
                AWS_SETTINGS.s3_bucket,
                s3_path
            )
        
        file_url = f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/{s3_path}"

        return file_url
    
    async def delete_image_in_S3(
        self,
        file_url : str
    ) -> dict : 
        
        s3_key = file_url.split(f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/")[-1]

        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region
        ) as s3_client:
            try:
                await s3_client.head_object(Bucket=AWS_SETTINGS.s3_bucket, Key=s3_key)
            except ClientError as e:
                # 파일이 존재하지 않을 경우 예외 처리
                if e.response["Error"]["Code"] == "404":
                    raise FileNotFoundError
                else:
                    raise UnexpectedError
                
            await s3_client.delete_object(Bucket=AWS_SETTINGS.s3_bucket, Key=s3_key)

        return {"message": f"Deleted image: {file_url}"}
    
    async def image_exists_in_S3(self, file_url: str | None) -> bool:
        """S3에서 이미지가 존재하는지 확인"""
        if not file_url :
            return False
        s3_key = file_url.split(f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/")[-1]

        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region
        ) as s3_client:
            try:
                await s3_client.head_object(Bucket=AWS_SETTINGS.s3_bucket, Key=s3_key)
                return True  # ✅ 파일이 존재하면 True 반환
            except ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    return False  # ✅ 파일이 존재하지 않으면 False 반환
                else:
                    raise UnexpectedError # 다른 에러는 그대로 발생

    async def generate_presigned_url(
        self,
        request : PresignedUrlRequest
    ) :
        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region
        ) as s3_client:
            unique_filename = f"{uuid.uuid4()}-{request.file_name}"
            
            # 비동기적으로 presigned URL 생성
            presigned_url = await s3_client.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": AWS_SETTINGS.s3_bucket,
                    "Key": f"uploads/{unique_filename}",
                    "ContentType": request.file_type,
                },
                ExpiresIn=3600  # URL 유효기간 (초 단위)
            )
            return {
                "presigned_url": presigned_url,
                "file_url": f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/uploads/{unique_filename}"
            }
        