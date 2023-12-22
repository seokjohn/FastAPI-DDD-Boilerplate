import typing
from typing import Optional, Tuple
import jwt

from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from sqlalchemy import select
from fastapi import Request
from fastapi.responses import JSONResponse

from core.config import SETTINGS
from core.db import session, standalone_session
from core.exceptions import (
    APIException,
    TokenExpiredEx,
    InvalidTokenEx,
    NotFoundUserEx,
    BlockedUserEx
)

from app.user.entity import Users
from app.user.enums.user import UserStatus
from app.user.repository import user_repository


def on_auth_error(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content=dict(
            status=exc.status_code,
            msg=exc.msg,
            msg_code=exc.msg_code,
            detail=exc.detail,
            code=exc.code
        ),
    )


async def check_authorization(user_id: str, user_email: str):
    user = await user_repository.find_by_id_and_email(user_id, user_email)
    if not user:
        return False, None
    if user.status == UserStatus.deleted:
        return False, None
    elif user.status == UserStatus.blocked:
        return False, None
    return True, user


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Tuple[bool, Optional[Users]]:
        current_user = None
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        token = authorization.replace("Bearer ", "")
        try:
            payload = jwt.decode(
                token,
                SETTINGS.JWT_SECRET_KEY,
                algorithms=[SETTINGS.JWT_ALGORITHM],
            )
            user_id = payload.get("id")
            user_email = payload.get("email")
        except Exception:
            return False, None

        return await check_authorization(user_id, user_email)


class AuthenticationMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        backend: AuthenticationBackend,
        on_error: typing.Optional[
            typing.Callable[[HTTPConnection, AuthenticationError], Response]
        ] = None,
    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = (on_error if on_error is not None else self.default_on_error)

    @standalone_session
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        try:
            auth_result = await self.backend.authenticate(conn)
        except AuthenticationError as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return

        if auth_result is None:
            auth_result = None, None
        conn.scope["auth"], conn.state.user = auth_result
        await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=400)