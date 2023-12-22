from core.exceptions import HTTPStatus, APIException


class BlockedUserEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            msg=f"차단된 유저 입니다.",
            msg_code="BLOCKED_USER",
            code=f"{HTTPStatus.FORBIDDEN}{'3'.zfill(4)}",
            ex=ex,
        )


class WithdrawalUserEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            msg=f"탈퇴한 유저 입니다.",
            msg_code=HTTPStatus.FORBIDDEN.description,
            code=f"{HTTPStatus.FORBIDDEN}{'4'.zfill(4)}",
            ex=ex,
        )


class NotFoundUserEx(APIException):
    def __init__(self, user_id: str = None, ex: Exception = None):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            msg=f"해당 유저를 찾을 수 없습니다.",
            msg_code=HTTPStatus.NOT_FOUND.description,
            detail={"userId": user_id},
            code=f"{HTTPStatus.NOT_FOUND}{'1'.zfill(4)}",
            ex=ex,
        )
