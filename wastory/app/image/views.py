import uuid
import aioboto3
from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Depends
from botocore.exceptions import ClientError
from typing import Annotated

from wastory.database.settings import AWSSettings
from wastory.app.user.models import User
from wastory.app.user.views import login_with_header
from wastory.app.image.dto.responses import ImageDetailResponse

# AWS 설정 불러오기
AWS_SETTINGS = AWSSettings()

image_router = APIRouter()

@image_router.post("/upload/", status_code = 201)
async def upload_image(
    file: UploadFile = File(...)
    ) -> ImageDetailResponse:
    try:

        unique_filename = f"{uuid.uuid4()}-{file.filename}"

        # S3 업로드 경로
        s3_path = f"uploads/{unique_filename}"

        # S3 비동기 클라이언트 생성 및 업로드
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

        # 업로드된 파일 URL 반환
        file_url = f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/{s3_path}"
    
        return ImageDetailResponse.from_image(file_url)
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 ClientError: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@image_router.delete("/delete/")
async def delete_image(file_url: str = Query(..., description="삭제할 S3 파일의 URL")) -> dict:
    try:
        # S3 경로 추출 (URL에서 파일 경로 추출)
        s3_key = file_url.split(f"https://{AWS_SETTINGS.s3_bucket}.s3.{AWS_SETTINGS.default_region}.amazonaws.com/")[-1]

        # S3 비동기 클라이언트 생성 및 삭제
        session = aioboto3.Session()
        async with session.client(
            "s3",
            aws_access_key_id=AWS_SETTINGS.access_key_id,
            aws_secret_access_key=AWS_SETTINGS.secret_access_key,
            region_name=AWS_SETTINGS.default_region
        ) as s3_client:
            await s3_client.delete_object(Bucket=AWS_SETTINGS.s3_bucket, Key=s3_key)

        return {"message": f"Deleted image: {file_url}"}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 ClientError: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
