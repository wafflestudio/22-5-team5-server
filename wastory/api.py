from fastapi import APIRouter

from wastory.app.user.views import user_router
from wastory.app.blog.views import blog_router
from wastory.app.category.views import category_router
from wastory.app.article.views import article_router
from wastory.app.notification.views import notification_router
from wastory.app.subscription.views import subscription_router
from wastory.app.like.views import like_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(blog_router, prefix="/blogs", tags=["blogs"])
api_router.include_router(category_router, prefix="/categories", tags=["categories"])
api_router.include_router(article_router, prefix="/articles", tags=["articles"])
api_router.include_router(notification_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(subscription_router, prefix="/subscription", tags=["subscriptions"])
api_router.include_router(like_router, prefix="/likes", tags=["likes"])

