from pydantic import BaseModel
from typing import List,Optional
from wastory.app.category.models import Category


class CategoryDetailResponse(BaseModel):
    id: int
    category_name: str
    level: int
    parent_id: Optional[int] = None  # 기본값 None
    child: Optional[List["CategoryDetailResponse"]] = None  # 기본값 None

    @staticmethod
    def from_category(category: Category) -> "CategoryDetailResponse":
        response = CategoryDetailResponse(
            id=category.id,
            category_name=category.name,
            level=category.level
        )
        # level == 2면 parent_id 설정
        if category.level == 2:
            response.parent_id = category.parent_id

        return response

class CategoryListResponse(BaseModel):
    id: int
    category_name: str
    level: int
    article_count: int
    # children: 하위 카테고리 리스트 (하위 카테고리도 같은 구조를 사용하되 children은 비게 됨)
    children: List["CategoryListResponse"] = []

    class Config:
        orm_mode = True
        # 재귀 모델 선언 시 필요
        allow_population_by_field_name = True

    @staticmethod
    def from_category(category, article_count: int) -> "CategoryListResponse":
        return CategoryListResponse(
            id=category.id,
            category_name=category.name,
            level=category.level,
            article_count=article_count,
            children=[]  # 하위 카테고리는 Service에서 채워줌
        )

class CategoryFinalResponse(BaseModel):
    category_list: List[CategoryListResponse] = []

    class Config:
        orm_mode = True

    @staticmethod
    def from_categorylist(category_list: List[CategoryListResponse]) -> "CategoryFinalResponse":
        return CategoryFinalResponse(
            category_list=category_list
        )