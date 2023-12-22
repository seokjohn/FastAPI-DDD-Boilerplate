from fastapi import APIRouter
from starlette.requests import Request

from api.auth.v1.request.auth import (
    GoogleLoginRequest,
)
from api.auth.v1.response.auth import (
    TokenResponse,
    GoogleTokenResponse
)
from app.user.services.oauth import user_oauth_service
from app.user.exceptions import (
    InvalidTokenEx,
    WithdrawalUserEx,
    NotFoundUserEx,
)
from core.fastapi.swagger import set_swagger

router = APIRouter()

@router.post(
    "/login/google",
    status_code=200,
    response_model=GoogleTokenResponse,
    responses=set_swagger(
        InvalidTokenEx,
        WithdrawalUserEx
    )
)
async def google_login(login_info: GoogleLoginRequest):
    """
        `구글 회원가입/로그인 API`\n
        :param login_info:
        :return:
    """
    token = await user_oauth_service.goog_login(
            login_info.id_token,
            login_info.region,
            login_info.language
        )
    return GoogleTokenResponse(**token)

'''
@router.post(
    "/refresh",
    status_code=200,
    response_model=TokenResponse, 
    responses=set_swagger(NotFoundUserEx))
async def check_refresh(refresh_token, request: Request):
    """
      `토큰 Refresh API`\n
      :param request:
      :param refresh_token:
      :return:
     """
    token = await user_service.refresh(refresh_token)
    return TokenResponse(**token)
'''