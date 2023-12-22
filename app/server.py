from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from api import router
from core.config import SETTINGS
from core.exceptions import APIException
from core.fastapi.middlewares import (
    on_auth_error,
    AuthenticationMiddleware,
    AuthBackend,
    DataDogMiddleware,
    SQLAlchemyMiddleware,
    ResponseLogMiddleware,
)
from core.helpers.cache import Cache, RedisBackend, CustomKeyMaker


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(APIException)
    async def custom_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=dict(
                status=exc.status_code,
                msg=exc.msg,
                msg_code=exc.msg_code,
                detail=exc.detail,
                code=exc.code
            ),
        )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
                allow_origins=SETTINGS.ALLOW_SITE,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
        ),
        Middleware(
            TrustedHostMiddleware(
                allowed_hosts=SETTINGS.ALLOW_SITE,
            )
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(ResponseLogMiddleware),
        #Middleware(AccessLoggerMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="FastAPI",
        description="FastAPI",
        version="0.0.1",
        docs_url="/swagger-ui",
        redoc_url="/redoc-ui",
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()

    app_.router.redirect_slashes = False
    return app_


app = create_app()
