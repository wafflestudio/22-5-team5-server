from functools import cache
from typing import Annotated, Sequence

from sqlalchemy import select, or_, and_
from wastory.app.article.errors import ArticleNotFoundError
from wastory.app.article.models import Article
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION

class ArticleStore :
    @transactional
    async def create_article(
        self, blog_id: int, category_id : int, atricle_title : str, article_content: str
    ) -> Article :
        # created_at, updated_at 은 자동반영되기에 따로 전달하지 않음.
        article = Article(
            blog_id = blog_id, category_id = category_id, title = atricle_title, content = article_content)
        SESSION.add(article)
        # 왜 필요하지?       
        SESSION.flush()
        return article
    
    @transactional
    async def update_article(
        self, 
        article: Article, 
        article_title: str | None = None,
        article_content: str | None = None,
    ) -> Article:
        if article_title is not None:
            article.title = article_title
        if article_content is not None:
            article.content = article_content
        return article

    @transactional
    async def delete_article(self, article: Article) -> None:
        if article is None: 
            raise ArticleNotFoundError()
        SESSION.delete(article)
        SESSION.flush()       

    @transactional
    async def get_article_by_id(self, article_id : int) -> Article | None:
        article = SESSION.get(Article, article_id)
        return article
    
    @transactional
    async def get_articles_by_ids(self, article_ids: list[int]) -> Sequence[Article]:
        article_list_query = select(Article).where(Article.id.in_(article_ids))
        return SESSION.scalars(article_list_query).all()
    
    @transactional
    async def get_articles_in_blog(self, blog_id: int) -> Sequence[Article]:
        query = select(Article).where(Article.blog_id == blog_id)
        return SESSION.scalars(query).all()
    
    @transactional
    async def get_articles_in_blog_in_category(
        self, 
        category_id: int,
        blog_id: int,
        ) -> Sequence[Article]:
        query = select(Article).where(
            Article.category_id == category_id,
            Article.blog_id == blog_id
            )
        return SESSION.scalars(query).all()
    
    @transactional
    async def get_articles_by_words_and_blog_id(
        self, 
        searching_words: str | None = None,
        blog_id: int | None = None
    ) -> Sequence[Article]:
    
        # 검색어가 없으면 빈 리스트 반환
        if not searching_words:
            return []
        
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
        
        # 모든 조건이 만족해야 함
        query = select(Article).where(and_(*search_conditions))
        
        # 쿼리 실행 및 결과 반환
        result = await SESSION.scalars(query)
        return result.all()

