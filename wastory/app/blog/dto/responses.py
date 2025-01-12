from pydantic import BaseModel, Field
from datetime import datetime

class BlogDetailResponse(BaseModel):
    id: int
    blog_name: str = Field(serialization_alias="blog_name")
    address_name: str = Field(serialization_alias="address_name")  # 주소 이름 필드 추가
    description: str | None = None  # 선택적 설명 필드
    created_at: datetime
    updated_at: datetime
    main_image_url: str | None = None  # 메인 이미지 URL 필드 추가
    user_id : int

    class Config:
        orm_mode = True  # SQLAlchemy 모델에서 데이터를 가져올 때 Pydantic 변환 지원
        allow_population_by_field_name = True  # 필드 이름을 정확히 사용하도록 강제
        extra = "allow"  # 모델에 없는 필드도 허용
        exclude_none = False  # None 값도 포함
