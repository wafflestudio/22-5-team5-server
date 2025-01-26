from typing import Annotated
from fastapi import APIRouter, Depends
from wastory.app.article.dto.requests import ArticleCreateRequest, ArticleUpdateRequest
from wastory.app.article.dto.responses import PaginatedArticleListResponse, ArticleDetailResponse, ArticleInformationResponse
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

    if article.category_id == 0:
        return await article_service.create_article(
            user=user, 
            article_title=article.title, 
            article_content=article.content, 
            article_description= article.description, 
            main_image_url = article.main_image_url,
            category_id=user_blog.default_category_id,
            hometopic_id = article.hometopic_id,
            secret=article.secret
            )
    else:
        return await article_service.create_article(
            user=user, 
            article_title=article.title, 
            article_content=article.content, 
            article_description = article.description,
            main_image_url = article.main_image_url, 
            category_id=article.category_id,
            hometopic_id = article.hometopic_id,
            secret=article.secret
            )

# article 수정
@article_router.patch("/update/{article_id}", status_code=200)
async def update_article(
    user: Annotated[User, Depends(login_with_header)],
    article_id: int,
    article: ArticleUpdateRequest,
    article_service: Annotated[ArticleService, Depends()],
    blog_service: Annotated[BlogService, Depends()],

) -> ArticleDetailResponse:
    user_blog = await blog_service.get_blog_by_user(user)
    if article.category_id == 0:
        return await article_service.update_article(
            user=user,
            article_id = article_id,
            article_title=article.title, 
            article_content=article.content, 
            article_description = article.description, 
            main_image_url = article.main_image_url,
            category_id=user_blog.default_category_id,
            hometopic_id = article.hometopic_id,
            secret=article.secret
        )
    else : 
        return await article_service.update_article(
            user=user, 
            article_id = article_id,
            article_title=article.title, 
            article_content=article.content, 
            article_description = article.description, 
            main_image_url = article.main_image_url,
            category_id=article.category_id,
            hometopic_id = article.hometopic_id
        )


# article 정보 가져오기
@article_router.get("/get/{article_id}", status_code=200)
async def get_article_information_by_id(
    article_service: Annotated[ArticleService, Depends()],
    user: Annotated[User, Depends(login_with_header)],
    article_id : int,
) -> ArticleInformationResponse :
    return await article_service.get_article_information_by_id(user, article_id)

# blog 내 인기글 가져오기
@article_router.get("/today_wastory", status_code=200)
async def get_today_most_viewed(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    page : int
) ->PaginatedArticleListResponse:
    return await article_service.get_today_most_viewed(
        page = page,
        user=user
    )
# blog 내 인기글 가져오기
@article_router.get("/weekly_wastory", status_code=200)
async def get_weekly_most_viewed(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
) ->PaginatedArticleListResponse:
    return await article_service.get_weekly_most_viewed()

# blog 내 인기글 가져오기
@article_router.get("/blogs/{blog_id}/sort_by/{sort_by}", status_code=200)
async def get_top_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    blog_id : int,
    sort_by: str
) ->PaginatedArticleListResponse:
    return await article_service.get_top_articles_in_blog(
        blog_id = blog_id,
        sort_by = sort_by,
        user=user
    )

# hometopic 인기글 가져오기기
@article_router.get("/hometopic/{hometopic_id}", status_code=200)
async def get_most_viewed_in_hometopic(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    high_hometopic_id : int,
    page: int
) ->PaginatedArticleListResponse:
    return await article_service.get_most_viewed_in_hometopic(
        high_hometopic_id = high_hometopic_id,
        page = page,
        user=user
    )


# blog 내 article 목록 가져오기
@article_router.get("/blogs/{blog_id}", status_code=200)
async def get_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    blog_id : int,
    page: int
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_in_blog(
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )

# blog 내 특정 category 내 article 목록 가져오기
@article_router.get("/blogs/{blog_id}/categories/{category_id}", status_code=200)
async def get_articles_in_blog_in_category(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    category_id : int,
    blog_id: int,
    page: int
) ->PaginatedArticleListResponse:
    per_page = 10

    return await article_service.get_articles_in_blog_in_category(
        category_id = category_id, 
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )
# blog 내 subscription 목록에서 article 가져오기
@article_router.get("/blogs/{blog_id}/subscription", status_code=200)
async def get_articles_of_subscription(
    user: Annotated[User, Depends(login_with_header)],
    article_service: Annotated[ArticleService, Depends()],
    page: int
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_of_subscriptions(
        user = user,
        page = page,
        per_page = per_page
    )

# blog 내 인기글 가져오기
@article_router.get("/blogs/{blog_id}/sort_by/{sort_by}", status_code=200)
async def get_top_articles_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    blog_id : int,
    sort_by: str
) ->PaginatedArticleListResponse:
    return await article_service.get_top_articles_in_blog(
        blog_id = blog_id,
        sort_by = sort_by,
        user=user
    )


# 특정 blog 내에서의 검색 기능 지원
@article_router.get("/search/{blog_id}/{searching_words}", status_code=200)
async def get_articles_by_words_in_blog(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    page: int,
    searching_words: str | None = None,
    blog_id : int | None = None
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_by_words_and_blog_id(
        searching_words = searching_words, 
        blog_id = blog_id,
        page = page,
        per_page = per_page,
        user=user
    )

# 전체 검색 기능 지원
@article_router.get("/search/{searching_words}", status_code=200)
async def get_articles_by_word(
    article_service: Annotated[ArticleService, Depends()],
    user : Annotated[User, Depends(login_with_header)],
    page: int,
    searching_words: str,
) -> PaginatedArticleListResponse:
    per_page = 10
    return await article_service.get_articles_by_words_and_blog_id(
        searching_words = searching_words, 
        blog_id = None,
        page = page,
        per_page = per_page,
        user=user
    )

# article 삭제
@article_router.delete("/delete/{article_id}", status_code=204)
async def delete_article(
    user: Annotated[User, Depends(login_with_header)],
    article_id: int,
    article_service: Annotated[ArticleService, Depends()],
) -> None:
    await article_service.delete_article(user, article_id)