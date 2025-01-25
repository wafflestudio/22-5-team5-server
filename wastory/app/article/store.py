from functools import cache
from typing import Annotated, Sequence
from datetime import datetime, timedelta
from sqlalchemy import select, or_, and_, func, update

from wastory.app.article.models import Article
from wastory.app.blog.models import Blog
from wastory.app.like.models import Like
from wastory.app.comment.models import Comment
from wastory.app.subscription.models import Subscription
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.article.dto.responses import ArticleSearchInListResponse, PaginatedArticleListResponse, ArticleInformationResponse

class ArticleStore :
    @transactional
    async def create_article(
        self, atricle_title : str, article_content: str, article_description: str, blog_id : int, category_id : int, hometopic_id : int 
    ) -> Article :
        article = Article(
            title = atricle_title, content = article_content, description = article_description, blog_id = blog_id, category_id = category_id, hometopic_id = hometopic_id
        )
        SESSION.add(article)
        # 왜 필요하지?       
        await SESSION.flush()
        await SESSION.refresh(article)
        return article
    
    @transactional
    async def update_article(
        self, 
        article: Article, 
        article_title: str | None = None,
        article_content: str | None = None,
        article_description: str | None = None,

    ) -> Article:
        if article_title is not None:
            article.title = article_title
        if article_content is not None:
            article.content = article_content
        if article_content is not None:
            article.description = article_description
        await SESSION.merge(article)
        await SESSION.flush()
        return article
    

    @transactional
    async def delete_article(self, article: Article) -> None:
        await SESSION.delete(article)
        await SESSION.flush()   

    @transactional
    async def increment_article_views(self, article_id: int) -> None:
        stmt = (
            update(Article)
            .where(Article.id == article_id)
            .values(views=Article.views + 1)
        )
        await SESSION.execute(stmt)
        await SESSION.flush()

    @transactional
    async def get_article_by_id(self, article_id : int) -> Article | None:
        article = await SESSION.get(Article, article_id)
        return article

    @transactional
    async def get_article_information_by_id(self, article_id : int) -> ArticleInformationResponse:

        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # likes 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # comments 조인
            .filter(Article.id == article_id)
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)

        )
        result = await SESSION.execute(stmt)

        row = result.one_or_none()
        article = ArticleInformationResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
        
        blog = await SESSION.get(Blog, article.blog_id)

        if article.category_id == blog.default_category_id:
            article.category_id = 0

        return article
    
    @transactional
    async def get_articles_by_ids(self, article_ids: list[int]) -> Sequence[Article]:
        article_list_query = select(Article).where(Article.id.in_(article_ids))
        result = await SESSION.scalars(article_list_query)  # await 추가
        return result.all()
    
    @transactional
    async def get_today_most_viewed(
        self,
        page: int,
    ) -> PaginatedArticleListResponse:
        # 정렬 기준: 조회수 내림차순
        sort_column = Article.views.desc()
        per_page = 1  # 페이지당 기사 수 (1개로 설정)
        offset = (page - 1) * per_page  # 페이지 오프셋 계산

        # 오늘 날짜의 시작과 끝 계산
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        print("today_start:", today_start)
        print("today_end:", today_end)


        # 쿼리 작성: 오늘 작성된 인기 글 가져오기
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # 좋아요 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # 댓글 조인
            .filter(
                Article.created_at >= today_start,           # 오늘 시작 시간 이후
                Article.created_at < today_end               # 오늘 끝 시간 이전
            )
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(sort_column)  # 조회수 기준 정렬
            .offset(offset)         # 페이지 오프셋 적용
            .limit(per_page)        # 페이지당 제한 (1개)
        )

        # 쿼리 실행
        result = await SESSION.execute(stmt)
        rows = result.all()

        
        # Pydantic 모델로 변환하여 반환 데이터 생성
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 기사 개수 계산 (페이지네이션을 위해)
        total_count_stmt = select(func.count(Article.id)).filter(
            Article.created_at >= today_start,
            Article.created_at < today_end
        )
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=page,
            per_page=per_page,  # 1페이지에 1개
            total_count=total_count or 0,
            articles=articles
        )

    @transactional
    async def get_weekly_most_viewed(
        self,
    ) -> PaginatedArticleListResponse:
        # 정렬 기준: 조회수 내림차순
        sort_column = Article.views.desc()
        per_page = 5  # 페이지당 기사 수


        # 일주일 전과 오늘 날짜 계산
        week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        # 쿼리 작성: 홈토픽 ID 목록에 속하고, 지난 일주일 동안 작성된 인기 글 가져오기
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # 좋아요 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # 댓글 조인
            .filter(
                Article.created_at >= week_start,            # 일주일 전 시작 시간 이후
                Article.created_at <= today_end              # 오늘 끝 시간 이전
            )
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(sort_column)  # 조회수 기준 정렬
            .limit(per_page)        # 페이지당 제한
        )

        # 쿼리 실행
        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환하여 반환 데이터 생성
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 기사 개수 계산 (페이지네이션을 위해)
        total_count_stmt = select(func.count(Article.id)).filter(
            Article.created_at >= week_start,
            Article.created_at <= today_end
        )
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=1,
            per_page=per_page,
            total_count=total_count or 0,
            articles=articles
        )
    
    
    # tistory 에서 hometopic 인기글을 7개씩 4개의 page 를 나열하기에, 동일하게 구현하였습니다.
    @transactional
    async def get_most_viewed_in_hometopic(
        self,
        hometopic_id_list: list[int],
        page: int,
    ) -> PaginatedArticleListResponse:
        # 정렬 기준: 조회수 내림차순
        sort_column = Article.views.desc()
        per_page = 7  # 페이지당 기사 수
        offset = (page - 1) * per_page  # 페이지 오프셋 계산

        # 쿼리 작성: 홈토픽 ID 목록에 속한 인기 글 가져오기
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # 좋아요 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # 댓글 조인
            .filter(Article.hometopic_id.in_(hometopic_id_list))  # 홈토픽 ID 필터링
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(sort_column)  # 조회수 기준 정렬
            .offset(offset)  # 페이지 오프셋 적용
            .limit(per_page)  # 페이지당 제한
        )

        # 쿼리 실행
        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환하여 반환 데이터 생성
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 인기 글 개수 계산 (페이지네이션을 위해)
        total_count_stmt = select(func.count(Article.id)).filter(
            Article.hometopic_id.in_(hometopic_id_list)
        )
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count or 0,
            articles=articles,
        )
    
    @transactional
    async def get_articles_in_blog(self, blog_id: int, page: int, per_page: int) -> PaginatedArticleListResponse:
        offset_val = (page - 1) * per_page

        # 쿼리 작성: Article에 likes와 comments를 조인하여 계산
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # likes 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # comments 조인
            .filter(Article.blog_id == blog_id)
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(Article.created_at.desc())
            .offset(offset_val)
            .limit(per_page)
        )

        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환하여 필요한 데이터만 반환
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 개수 계산
        total_count_stmt = select(func.count(Article.id)).filter(Article.blog_id == blog_id)
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count or 0,
            articles=articles,
        )
    
    @transactional
    async def get_top_articles_in_blog(
        self,
        blog_id: int,
        sort_by: str = "views",  # 기본 정렬 기준은 "likes" 
        top_n: int = 20          # 기본 상위 20개 가져오기
    ) -> PaginatedArticleListResponse:
        # 정렬 기준 설정
        if sort_by == "likes":
            sort_column = func.count(Like.id).desc()
        elif sort_by == "comments":
            sort_column = func.count(Comment.id).desc()
        elif sort_by == "views":
            sort_column = Article.views.desc()  # 조회수를 기준으로 정렬
        else:
            raise ValueError("Invalid sort_by value. Use 'likes' or 'comments' or 'views'.")

        # 쿼리 작성: 특정 블로그에서 좋아요 또는 댓글 기준으로 상위 N개 가져오기
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # likes 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # comments 조인
            .filter(Article.blog_id == blog_id)  # 특정 블로그에서 필터링
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(sort_column)  # 좋아요 순 또는 댓글 순으로 정렬
            .limit(top_n)           # 상위 N개 제한
        )

        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환하여 필요한 데이터만 반환
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        return PaginatedArticleListResponse(
            page=1,  # 인기글은 페이지 구분 없이 한 번에 반환
            per_page=top_n,
            total_count=len(articles),
            articles=articles,
        )
        
    @transactional
    async def get_articles_in_blog_in_category(
        self,
        category_id: int,
        blog_id: int,
        page: int,
        per_page: int
    ) -> PaginatedArticleListResponse:

        # category_id가 0일 경우, blog의 default_category_id로 설정
        if category_id == 0:
            blog = await SESSION.get(Blog, blog_id)
            category_id = blog.default_category_id
        
        
        offset_val = (page - 1) * per_page

        # 쿼리 작성: Article에 likes와 comments를 조인하여 계산
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # likes 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # comments 조인
            .filter(
                Article.category_id == category_id,  # category_id 필터
                Article.blog_id == blog_id           # blog_id 필터
            )
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(Article.created_at.desc())
            .offset(offset_val)
            .limit(per_page)
        )

        # 쿼리 실행
        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 개수 계산
        total_count_stmt = select(func.count(Article.id)).filter(
            Article.category_id == category_id,
            Article.blog_id == blog_id
        )
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count or 0,
            articles=articles,
        )   
    
    @transactional
    async def get_articles_by_words_and_blog_id(
        self,
        searching_words: str | None = None,
        blog_id: int | None = None,
        page: int = 1,
        per_page: int = 10
    ) -> PaginatedArticleListResponse:
        # 검색어가 없으면 빈 리스트와 0 개수 반환
        if not searching_words:
            return PaginatedArticleListResponse(
                page=page,
                per_page=per_page,
                total_count=0,
                articles=[]
            )

        # 검색어를 공백으로 분리
        words = searching_words.split()

        # 제목과 내용 중 하나라도 단어를 포함해야 함
        search_conditions = [
            or_(
                Article.title.ilike(f"%{word}%"),
                Article.content.ilike(f"%{word}%")
            )
            for word in words
        ]

        # 블로그 ID가 있는 경우, 블로그 ID 조건 추가
        if blog_id is not None:
            search_conditions.append(Article.blog_id == blog_id)

        # 오프셋 계산
        offset_val = (page - 1) * per_page

        # 쿼리 작성: Article에 likes와 comments를 조인하여 검색
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # likes 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # comments 조인
            .where(and_(*search_conditions))  # 검색 조건 적용
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(Article.created_at.desc())
            .offset(offset_val)
            .limit(per_page)
        )

        # 쿼리 실행 및 결과 처리
        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 개수 계산
        total_count_stmt = select(func.count(Article.id)).where(and_(*search_conditions))
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count or 0,
            articles=articles,
        )
    
    @transactional
    async def get_articles_of_subscriptions(
        self, blog_id: int, page: int, per_page: int
    ) -> PaginatedArticleListResponse:
        offset_val = (page - 1) * per_page

        # 구독한 블로그 ID 가져오기
        subscribed_blogs_stmt = (
            select(Subscription.subscribed_id)
            .filter(Subscription.subscriber_id == blog_id)
        )
        subscribed_ids_result = await SESSION.scalars(subscribed_blogs_stmt)
        subscribed_ids = subscribed_ids_result.all()

        if not subscribed_ids:
            # 구독한 블로그가 없으면 빈 결과 반환
            return PaginatedArticleListResponse(
                page=page,
                per_page=per_page,
                total_count=0,
                articles=[]
            )

        # 구독한 블로그들의 Article 가져오기
        stmt = (
            select(
                Article,
                func.count(Like.id).label("likes"),
                func.count(Comment.id).label("comments"),
                Blog.blog_name.label("blog_name"),
                Blog.main_image_url.label("blog_main_image_url")
            )
            .join(Blog, Blog.id == Article.blog_id)
            .join(Like, Like.article_id == Article.id, isouter=True)  # likes 조인
            .join(Comment, Comment.article_id == Article.id, isouter=True)  # comments 조인
            .filter(Article.blog_id.in_(subscribed_ids))  # 구독한 블로그의 Article만 필터
            .group_by(Article.id, Blog.blog_name, Blog.main_image_url)
            .order_by(Article.created_at.desc())  # 최신순 정렬
            .offset(offset_val)
            .limit(per_page)
        )

        result = await SESSION.execute(stmt)
        rows = result.all()

        # Pydantic 모델로 변환하여 필요한 데이터만 반환
        articles = [
            ArticleSearchInListResponse.from_article(
                article=row.Article,
                blog_name = row.blog_name,
                blog_main_image_url = row.blog_main_image_url,
                article_likes=row.likes,
                article_comments=row.comments,
            )
            for row in rows
        ]

        # 전체 개수 계산
        total_count_stmt = select(func.count(Article.id)).filter(Article.blog_id.in_(subscribed_ids))
        total_count = await SESSION.scalar(total_count_stmt)

        return PaginatedArticleListResponse(
            page=page,
            per_page=per_page,
            total_count=total_count or 0,
            articles=articles,
        )
