from typing import Annotated

from fastapi import Depends
from wastory.app.category.store import CategoryStore
from wastory.app.category.dto.responses import CategoryDetailResponse,CategoryListResponse,CategoryFinalResponse
from wastory.app.category.errors import BlogNotFoundError
from wastory.app.user.models import User
from wastory.app.user.store import UserStore
from wastory.app.blog.store import BlogStore
from wastory.app.category.models import Category
class CategoryService:
    def __init__(
        self, 
        category_store: Annotated[CategoryStore, Depends()],
        user_store:Annotated[UserStore,Depends()],
        blog_store:Annotated[BlogStore,Depends()]) -> None:
        self.category_store = category_store
        self.user_store=user_store
        self.blog_store=blog_store

    async def create_category(
        self, categoryname:str, categorylevel:int, parentId:int,user:User
        )-> CategoryDetailResponse:
            user_blog=await self.blog_store.get_blog_of_user(user.id)  #이건 블로그 코드랑 합쳐야 함
            
            if user_blog is None:
                raise BlogNotFoundError()
            new_category= await self.category_store.create_category(
                blog_id=user_blog.id,categoryname=categoryname, categorylevel=categorylevel, parentId=parentId
            )
            return CategoryDetailResponse.from_category(new_category)

    async def update_category(
        self, category_id:int, new_category_name:str,user:User
    )-> CategoryDetailResponse:
        updated_category= await self.category_store.update_category(
                user=user,
                category_id=category_id,
                new_category_name=new_category_name
            )
        return CategoryDetailResponse.from_category(updated_category) #고쳐야 함

    async def delete_category(
        self, user:User, category_id:int
    )->None:
        await self.category_store.delete_category(user, category_id)

    async def list_categories(self, user: User) -> CategoryFinalResponse:
    # level=1 카테고리만 가져오되, 자식( level=2 )을 Eager Loading
        categories = await self.category_store.get_category_of_blog(user.blogs.id)
        
        category_list_responses = []
        for cat in categories:
            # 상위 카테고리의 article_count
            parent_article_count = await self.comment_store.get_article_count(cat.id)
            parent_resp = CategoryListResponse.from_category(cat, parent_article_count)

            # 자식 카테고리( level=2 ) 처리
            child_resp_list = []
            for child_cat in cat.children:
                child_article_count = await self.comment_store.get_article_count(child_cat.id)
                child_resp = CategoryListResponse.from_category(child_cat, child_article_count)
                child_resp_list.append(child_resp)

            # 상위 카테고리에 자식 리스트 할당
            parent_resp.children = child_resp_list
            
            category_list_responses.append(parent_resp)

        return CategoryFinalResponse.from_categorylist(category_list_responses)

    async def list_categories_by_blog(self, blog_id: int) -> CategoryFinalResponse:
    # level=1 카테고리만 가져오되, 자식( level=2 )을 Eager Loading
        categories = await self.category_store.get_category_of_blog(blog_id)
        
        category_list_responses = []
        for cat in categories:
            # 상위 카테고리의 article_count
            parent_article_count = await self.category_store.get_article_count(cat.id)
            parent_resp = CategoryListResponse.from_category(cat, parent_article_count)

            # 자식 카테고리( level=2 ) 처리
            child_resp_list = []
            for child_cat in cat.children:
                child_article_count = await self.category_store.get_article_count(child_cat.id)
                child_resp = CategoryListResponse.from_category(child_cat, child_article_count)
                child_resp_list.append(child_resp)

            # 상위 카테고리에 자식 리스트 할당
            parent_resp.children = child_resp_list
            
            category_list_responses.append(parent_resp)

        return CategoryFinalResponse.from_categorylist(category_list_responses)


