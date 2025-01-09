from pydantic import BaseModel
from typing import List, Optional

from wastory.app.category.models import Category


def _build_child_responses(children: List[Category]) -> List["CategoryDetailResponse"]:
    return [CategoryDetailResponse.from_category(child) for child in children]


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
        else:
            # level == 1이면 children을 재귀적으로 변환
            response.child = _build_child_responses(category.children)

        return response


class CategoryListResponse(BaseModel):
    id: int
    category_name: str
    level: int
    child_list: Optional[List[CategoryDetailResponse]] = None  # 기본값 None

    @staticmethod
    def from_category(category: Category) -> "CategoryListResponse":
        response = CategoryListResponse(
            id=category.id,
            category_name=category.name,
            level=category.level
        )
        # level == 1이면 하위 카테고리 리스트 변환
        if category.level == 1:
            response.child_list = _build_child_responses(category.children)

        return response