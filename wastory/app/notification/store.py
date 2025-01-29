from functools import cache
from typing import Annotated, List, Tuple, Optional

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from wastory.app.blog.errors import (
    BlogNotFoundError,
    BlognameAlreadyExistsError
)
from wastory.app.user.models import User
from wastory.app.blog.models import Blog
from wastory.app.notification.models import Notification
from wastory.app.article.models import Article
from wastory.app.comment.models import comment
from wastory.app.notification.dto.responses import NotificationResponse, PaginatedNotificationListResponse
from wastory.database.annotation import transactional
from wastory.database.connection import SESSION
from wastory.app.user.service import UserService


class NotificationStore:
    user_service=UserService
    @transactional
    async def add_notification(self, ids: List[Tuple[int, int]], type : int, username: str, notification_blogname: str, description: str | None, article_) -> Notification:
        max_description_length = 50
        if len(description) > max_description_length:
            description = description[:max_description_length - 3] + "..."
        description = "\"" + description + "\""

        notification_title = username
        if type == 1:
            notification_title = notification_title + "님이 새 글을 발행했습니다."
        if type == 2:
            notification_title = notification_title + "님이 내 블로그를 구독합니다."
        if type == 3:
            notification_title = notification_title + "님이 댓글을 남겼습니다."
        if type == 4:
            notification_title = notification_title + "님이 방명록을 남겼습니다."
        if type == 5:
            notification_title = notification_title + "님이 쪽지를 보냈습니다."

        notifications = [
            Notification(
                notification_type=type,
                notification_title=notification_title,
                notification_blogname=notification_blogname,
                description=description,
                user_id=user_id,
                blog_id=blog_id
            )
            for user_id, blog_id in ids
        ]
        SESSION.add_all(notifications)
        await SESSION.flush()
        for notification in notifications:
            await SESSION.refresh(notification)
        return notifications
    

    async def get_notification_by_id(self, notification_id: int) -> Notification | None:
        return await SESSION.scalar(select(Notification).where(Notification.id == notification_id))


    async def get_notifications_of_user(self, user_id: int, page: int, per_page: int, type: Optional[int] = None) -> PaginatedNotificationListResponse | None:
        offset_val = (page - 1) * per_page
        # 쿼리
        stmt = (
            select(
                Notification,
                User.username,
                Blog.main_image_url
            )
            .join(User, User.id == Notification.user_id)  # Notification과 User 조인
            .join(Blog, Blog.id == Notification.blog_id) 
            .where(Notification.user_id == user_id)  # user_id 필터
            .order_by(Notification.created_at.desc())  # 최신순 정렬
            .offset(offset_val)
            .limit(per_page)
        )

        # 유형 필터 추가
        if type is not None:
            stmt = stmt.where(Notification.notification_type == type)

        # 쿼리 실행
        notifications_result = await SESSION.execute(stmt)
        notifications = notifications_result.fetchall()

        # 총 알림 개수 계산
        total_notifications_stmt = select(func.count(Notification.id)).where(Notification.user_id == user_id)
        total_notifications = await SESSION.scalar(total_notifications_stmt)

        # Notification 객체를 NotificationResponse로 변환
        notifications_response = [
            NotificationResponse(
                id=n[0].id,
                notification_blogname=n[0].notification_blogname,
                notification_type=n[0].notification_type,
                notification_title=n[0].notification_title,
                description=n[0].description,
                created_at=n[0].created_at,
                updated_at=n[0].updated_at,
                checked=n[0].checked,
                username=n[1],
                blog_main_image_url=n[2]
            )
            for n in notifications
        ]

        return PaginatedNotificationListResponse(
            page=page,
            per_page=per_page,
            total_count=total_notifications,
            notifications=notifications_response,
        )


    @transactional
    async def delete_notification(self, notification_id: int) -> None:
        notification = await self.get_notification_by_id(notification_id=notification_id)
        await SESSION.delete(notification)
        await SESSION.flush() 


    @transactional
    async def check_notification(self, notification: Notification) -> Notification:
        if notification.checked == True:
            return notification
        notification.checked = True

        return notification