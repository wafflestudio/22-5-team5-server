from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,HTTP_204_NO_CONTENT


from wastory.app.user.models import User
guestbook_router = APIRouter()
from wastory.app.user.views import login_with_header

@guestbook_router.post("/create", status_code=HTTP_201_CREATED)
async def create(
    user:Annotated[User,Depends(login_with_header)],
    guestbook_service: Annotated[GuestbookService,Depends()]
)-> None:
    return await guestbook_service.create_guestbook(
        user=user
    )


