from pydantic import BaseModel
from typing import List, Optional

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
    children: List[CategoryDetailResponse]=[]
    class Config:
            orm_mode=True

    @staticmethod
    def from_category(category: Category) -> "CategoryListResponse":
        return CategoryListResponse(
            id=category.id,
            category_name=category.name,
            children=[CategoryDetailResponse.from_category(category) for category in category.children]
        )

class CategoryFinalResponse(BaseModel):
    category_list:List[CategoryListResponse]=[]
    class Config:
            orm_mode=True
    @staticmethod
    def from_categorylist(category_list:List[CategoryListResponse])->"CategoryFinalResponse":
        return CategoryFinalResponse(
            category_list=category_list
        )