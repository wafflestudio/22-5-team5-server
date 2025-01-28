from typing import Annotated, Optional
from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from authlib.integrations.starlette_client import OAuth
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from fastapi.responses import RedirectResponse

from wastory.database.settings import PW_SETTINGS
from wastory.app.user.dto.requests import UserSignupRequest, UserUpdateRequest, UserSigninRequest, PasswordUpdateRequest, UserEmailRequest, UserEmailVerifyRequest
from wastory.app.user.dto.responses import MyProfileResponse, UserSigninResponse, EmailVerifyResponse
from wastory.app.user.errors import InvalidTokenError
from wastory.app.user.models import User
from wastory.app.user.service import UserService

user_router = APIRouter()

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)
oauth = OAuth()
oauth.register(
    name="kakao",
    client_id=PW_SETTINGS.kakao_rest_api_key,  # 카카오 REST API 키
    access_token_url="https://kauth.kakao.com/oauth/token",   
    authorize_url="https://kauth.kakao.com/oauth/authorize",
    client_kwargs={"scope": "profile_nickname"},
)

#로그인을 한  경우랑 안  한 경우에 대 다른 처리를위해 추가했습니다.
async def optional_login_with_header(
    user_service: Annotated[UserService, Depends()],
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security_optional)]
) -> Optional[User]:
    if credentials is None:
        return None
    
    token = credentials.credentials
    email = user_service.validate_access_token(token)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise InvalidTokenError()
    return user

async def login_with_header(
    user_service: Annotated[UserService, Depends()],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    token = credentials.credentials
    email = user_service.validate_access_token(token)
    user = await user_service.get_user_by_email(email)
    if not user:
        raise InvalidTokenError()
    return user


@user_router.get("/auth/kakao")
async def login_via_kakao(request: Request):
    # redirect_uri = "wastory://authSuccess"
    # return await oauth.kakao.authorize_redirect(request, redirect_uri)
    redirect_uri = request.url_for("api_users_auth_kakao_callback")
    state = "random-generated-state"  # 고유한 state 값 생성
    request.session['state'] = state  # 세션에 저장
    return await oauth.kakao.authorize_redirect(request, redirect_uri, state=state)




@user_router.get("/auth/kakao/callback", name="api_users_auth_kakao_callback")
async def auth_kakao_callback(request: Request, user_service: Annotated[UserService, Depends()]):
    token = await oauth.kakao.authorize_access_token(request)
    user_info = await oauth.kakao.get("https://kapi.kakao.com/v2/user/me", token=token)
    user_info = user_info.json()

    nickname = user_info["properties"]["nickname"]
    user = await user_service.get_user_by_nickname(nickname)
    if user == None:
        await user_service.add_user(
            nickname, None
        )
        await user_service.update_user(
            username=nickname, nickname=nickname, email=nickname
        )
        access_token, refresh_token = user_service.issue_tokens(nickname)
    else:
        access_token, refresh_token = user_service.issue_tokens(user.email)

    return RedirectResponse(
        url=f"wastory://authSuccess?access_token={access_token}&refresh_token={refresh_token}"
    )


@user_router.post("/request-verification")
async def request_verification(
    email_request: UserEmailRequest, user_service: Annotated[UserService, Depends()]
):
    await user_service.send_verification_code(email_request.email)
    return "Success"


@user_router.post("/verify-email")
async def verify_email(
    verification_request: UserEmailVerifyRequest, user_service: Annotated[UserService, Depends()]
):
    is_valid = user_service.verify_code(verification_request.email, verification_request.code)
    return is_valid
    

@user_router.post("/email-exists")
async def email_exists(
    email_request: UserEmailRequest, user_service: Annotated[UserService, Depends()]
) -> EmailVerifyResponse:
    user = await user_service.get_user_by_email(email_request.email)
    return EmailVerifyResponse(verification=(user is not None))


@user_router.post("/signup", status_code=HTTP_201_CREATED)
async def signup(
    signup_request: UserSignupRequest, user_service: Annotated[UserService, Depends()]
):
    await user_service.add_user(
        signup_request.email, signup_request.password
    )
    return "Success"


@user_router.post("/signin", status_code=HTTP_200_OK)
async def signin(
    user_service: Annotated[UserService, Depends()],
    signin_request: UserSigninRequest,
):
    access_token, refresh_token = await user_service.signin(
        signin_request.email, signin_request.password
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
        username=update_request.username,
        email=user.email,
        nickname=user.nickname
    )
    return "Success"


@user_router.delete("/me")
async def delete_me(
    user: Annotated[User, Depends(login_with_header)],
    user_service: Annotated[UserService, Depends()],
):
    await user_service.delete_user(user.id)
    return "Success"


@user_router.patch("/change_password", status_code=HTTP_200_OK)
async def change_password(
    user: Annotated[User, Depends(login_with_header)],
    update_request: PasswordUpdateRequest,
    user_service: Annotated[UserService, Depends()],
):
    await user_service.update_password(
        email = user.email,
        old_password=update_request.old_password,
        new_password=update_request.new_password
    )
    return "Success"
