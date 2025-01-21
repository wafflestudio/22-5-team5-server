from typing import Annotated
from fastapi import APIRouter, Depends
from wastory.app.article.dto.requests import ArticleCreateRequest, ArticleUpdateRequest
from wastory.app.article.dto.responses import PaginatedArticleListResponse, ArticleDetailResponse, ArticleSearchInListResponse
from wastory.app.article.service import ArticleService
from wastory.app.blog.service import BlogService

from wastory.app.user.models import User
from wastory.app.user.views import login_with_header


article_router = APIRouter()

# article 생성
@article_router.post("/create", status_code=201)
async def create_article(
    user: Annotated[User, Depends(login_with_header)],
    article: ArticleCreateRequest,
    article_service: Annotated[ArticleService, Depends()],
    blog_service: Annotated[BlogService, Depends()],
) -> ArticleDetailResponse:
    user_blog = await blog_service.get_blog_by_user(user)
    print("default : ", user_blog.default_category_id)
    if article.category_id == 0:
        return await article_service.create_article(user=user, article_title=article.title, article_content=article.content, article_description= article.description, category_id=user_blog.default_category_id)
    else:
        return await article_service.create_article(user=user, article_title=article.title, article_content=article.content, article_description = article.description, category_id=article.category_id)

# article 수정
@article_router.patch("/update/{article_id}", status_code=200)
async def update_article(
    user: Annotated[User, Depends(login_with_header)],
    article_id: int,
    article: ArticleUpdateRequest,
    article_service: Annotated[ArticleService, Depends()],
) -> ArticleDetailResponse:
    return await article_service.update_article(
        user, article_id, article.title, article.content
    )

# article 정보 가져오기
@article_router.get("/get/{article_id}", status_code=200)
async def get_article_by_id(
    article_service: Annotated[ArticleService, Depends()],
    article_id : int,
) -> ArticleDetailResponse :
    return await article_service.get_article_by_id(article_id)

# blog 내 article 목록 가져오기
@article_router.get("/blogs/{blog_id}", status_code=200)
async def get_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    blog_id : int,
    page: int
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_in_blog(
        blog_id = blog_id,
        page = page,
        per_page = per_page
    )

# blog 내 특정 category 내 article 목록 가져오기
@article_router.get("/blogs/{blog_id}/categories/{category_id}", status_code=200)
async def get_articles_in_blog_in_category(
    article_service: Annotated[ArticleService, Depends()],
    category_id : int,
    blog_id: int,
    page: int
) ->PaginatedArticleListResponse:
    per_page = 10

    return await article_service.get_articles_in_blog_in_category(
        category_id = category_id, 
        blog_id = blog_id,
        page = page,
        per_page = per_page
    )

# 특정 blog 내에서의 검색 기능 지원
@article_router.get("/search/{blog_id}/{searching_words}", status_code=200)
async def get_articles_by_words_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    page: int,
    searching_words: str | None = None,
    blog_id : int | None = None
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_by_words_and_blog_id(
        searching_words = searching_words, 
        blog_id = blog_id,
        page = page,
        per_page = per_page
    )

# 전체 검색 기능 지원
@article_router.get("/search/{searching_words}", status_code=200)
async def get_articles_by_word(
    article_service: Annotated[ArticleService, Depends()],
    page: int,
    searching_words: str,
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_by_words_and_blog_id(
        searching_words = searching_words, 
        blog_id = None,
        page = page,
        per_page = per_page
    )

# article 삭제
@article_router.delete("/delete/{article_id}", status_code=204)
async def delete_article(
    user: Annotated[User, Depends(login_with_header)],
    article_id: int,
    article_service: Annotated[ArticleService, Depends()],
) -> None:
    await article_service.delete_article(user, article_id)