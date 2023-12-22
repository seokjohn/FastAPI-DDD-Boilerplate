from core.exceptions import HTTPStatus, APIException


class TokenExpiredEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            msg=f"토큰이 만료 되었습니다.",
            msg_code="TOKEN_EXPIRED",
            code=f"{HTTPStatus.UNAUTHORIZED}{'2'.zfill(4)}",
            ex=ex,
        )


class InvalidTokenEx(APIException):
    def __init__(self, msg: str = None, ex: Exception = None):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            msg=f"유효하지 않은 토큰입니다.{msg}",
            msg_code=HTTPStatus.UNAUTHORIZED.description,
            code=f"{HTTPStatus.UNAUTHORIZED}{'3'.zfill(4)}",
            ex=ex,
        )