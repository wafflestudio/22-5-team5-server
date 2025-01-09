from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from authlib.integrations.starlette_client import OAuth
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from wastory.app.user.dto.requests import UserSignupRequest, UserUpdateRequest, UserSigninRequest, UserSigninRequest, PasswordUpdateRequest
from wastory.app.user.dto.responses import MyProfileResponse, UserSigninResponse
from wastory.app.user.errors import InvalidTokenError, UserSigninResponse
from wastory.app.user.errors import InvalidTokenError
from wastory.app.user.models import User
from wastory.app.user.service import UserService

user_router = APIRouter()

security = HTTPBearer()

# async def login_with_header(
#     x_wapang_username: Annotated[str, Header(...)],
#     x_wapang_password: Annotated[str, Header(...)],
#     user_service: Annotated[UserService, Depends()],
# ) -> User:
#     user = await user_service.get_user_by_username(x_wapang_username)
#     if not user or user.password != x_wapang_password:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#         )
#     return user

security = HTTPBearer()

oauth = OAuth()
oauth.register(
    name="kakao",
    client_id="1184125",  # 카카오 REST API 키
    client_secret="YOUR_KAKAO_CLIENT_SECRET",  # 선택 사항
    access_token_url="https://kauth.kakao.com/oauth/token",
    authorize_url="https://kauth.kakao.com/oauth/authorize",
    client_kwargs={"scope": "profile_nickname"},
)

# async def login_with_header(
#     x_wapang_username: Annotated[str, Header(...)],
#     x_wapang_password: Annotated[str, Header(...)],
#     user_service: Annotated[UserService, Depends()],
# ) -> User:
#     user = await user_service.get_user_by_username(x_wapang_username)
#     if not user or user.password != x_wapang_password:
#         raise HTTPException(
#             status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#         )
#     return user


async def login_with_header(
    user_service: Annotated[UserService, Depends()],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    token = credentials.credentials
    username = user_service.validate_access_token(token)
    user = await user_service.get_user_by_username(username)
    if not user:
        raise InvalidTokenError()
    return user


@user_router.get("/auth/kakao")
async def login_via_kakao(request: Request):
    redirect_uri = request.url_for("api_users_auth_kakao_callback")
    return await oauth.kakao.authorize_redirect(request, redirect_uri)


@user_router.get("/auth/kakao/callback")
async def auth_kakao_callback(request: Request, user_service: Annotated[UserService, Depends()]):
    token = await oauth.kakao.authorize_access_token(request)
    user_info = await oauth.kakao.get("https://kapi.kakao.com/v2/user/me", token=token)
    user_info = user_info.json()

    nickname = user_info["properties"]["nickname"]
    username = await user_service.get_user_by_nickname(nickname)
    access_token, refresh_token = await user_service.issue_tokens(username)

    return UserSigninResponse(access_token=access_token, refresh_token=refresh_token)


@user_router.post("/signup", status_code=HTTP_201_CREATED)
async def signup(
    signup_request: UserSignupRequest, user_service: Annotated[UserService, Depends()]
):
    await user_service.add_user(
        signup_request.username, signup_request.password, signup_request.email
    )
    return "Success"


@user_router.post("/signin", status_code=HTTP_200_OK)
async def signin(
    user_service: Annotated[UserService, Depends()],
    signin_request: UserSigninRequest,
):
    access_token, refresh_token = await user_service.signin(
        signin_request.username, signin_request.password
    )
    return UserSigninResponse(access_token=access_token, refresh_token=refresh_token)


@user_router.get("/refresh", status_code=HTTP_200_OK)
async def refresh(
    user_service: Annotated[UserService, Depends()],
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    refresh_token = credentials.credentials
    access_token, new_refresh_token = await user_service.reissue_tokens(refresh_token)
    return UserSigninResponse(access_token=access_token, refresh_token=new_refresh_token)


@user_router.get("/me", status_code=HTTP_200_OK)
async def me(user: Annotated[User, Depends(login_with_header)]) -> MyProfileResponse:
    return MyProfileResponse.from_user(user)


@user_router.patch("/me", status_code=HTTP_200_OK)
async def update_me(
    user: Annotated[User, Depends(login_with_header)],
    update_request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends()],
):
    await user_service.update_user(
        user.username,
        email=update_request.email,
        address=update_request.address,
        phone_number=update_request.phone_number,
    )
    return "Success"


@user_router.patch("/change_password", status_code=HTTP_200_OK)
async def update_me(
    user: Annotated[User, Depends(login_with_header)],
    update_request: PasswordUpdateRequest,
    user_service: Annotated[UserService, Depends()],
):
    if user.password == update_request.old_password:
        await user_service.update_password(
            user.username,
            new_password=update_request.new_password
        )
    return "Success"