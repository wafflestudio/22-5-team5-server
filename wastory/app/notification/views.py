from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from wastory.app.notification.dto.requests import NotificationDeleteRequest, NotificationCheckRequest
from wastory.app.notification.dto.responses import NotificationResponse, NotificationListResponse
from wastory.app.user.models import User
from wastory.app.notification.models import Notification
from wastory.app.notification.service import NotificationService
from wastory.app.user.views import login_with_header

notification_router = APIRouter()


@notification_router.get("/my_notifications")
async def get_notifications_by_user(
    user: Annotated[User, Depends(login_with_header)],
    notification_service: Annotated[NotificationService, Depends()]
):
    notifications: list[Notification] = await notification_service.get_notifications_by_user(user)
    response = NotificationListResponse(
        total_count=len(notifications),
        notifications=[NotificationResponse.from_notification(n) for n in notifications]
    )
    return response

@notification_router.delete("/my_notifications")
async def delete_notification(
    notification_delete_request: NotificationDeleteRequest,
    notification_service: Annotated[NotificationService, Depends()]
)->str:
    await notification_service.delete_notification_by_id(notification_id=notification_delete_request.notification_id)
    return "Success"

@notification_router.patch("/my_notifications")
async def check_notification(
    user: Annotated[User, Depends(login_with_header)],
    notification_check_request: NotificationCheckRequest,
    notification_service: Annotated[NotificationService, Depends()]
) -> str:
    await notification_service.check_notification(notification_id=notification_check_request.notification_id)
    return "Success"