from fastapi import APIRouter

from wastory.app.user.views import user_router
from wastory.app.blog.views import blog_router
from wastory.app.category.views import category_router
from wastory.app.article.views import article_router
from wastory.app.comment.views import comment_router
from wastory.app.guestbook.views import guestbook_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(blog_router, prefix="/blogs", tags=["blogs"])
api_router.include_router(category_router, prefix="/categories", tags=["categories"])
api_router.include_router(article_router, prefix="/articles", tags=["articles"])
api_router.include_router(comment_router, prefix="/comments", tags=["comments"])
api_router.include_router(guestbook_router, prefix="/guestbook", tags=["guestbook"])

