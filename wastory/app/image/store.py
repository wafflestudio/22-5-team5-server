import aioboto3

from functools import cache
from typing import Annotated, Sequence
from fastapi import File, UploadFile

from sqlalchemy import select, or_, and_, func, update
from wastory.database.annotation import transactional
from wastory.database.settings import AWSSettings

from wastory.app.image.errors import FileNotFoundError, UnexpectedError
from botocore.exceptions import ClientError

AWS_SETTINGS = AWSSettings()

class ImageStore :
    async def upload_image(
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
    
    async def delete_image(
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
        