from http import HTTPStatus


class StatusCode:
    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    HTTP_409 = 409


DEFALUT_STATUS_RESPONSE_INFO = {
    HTTPStatus.BAD_REQUEST: {
        "description": "Bad Request",
        "content": {"application/json": {"examples": {}}},
    },
    StatusCode.HTTP_401: {
        "description": "Not Authorized",
        "content": {"application/json": {"examples": {}}}
    },
    StatusCode.HTTP_403: {
        "description": "Not Allowed",
        "content": {"application/json": {"examples": {}}}
    },
    StatusCode.HTTP_404: {
        "description": "Not Found",
        "content": {"application/json": {"examples": {}}}
    },
    StatusCode.HTTP_409: {
        "description": "Conflict",
        "content": {"application/json": {"examples": {}}}
    },
}


class APIException(Exception):
    status_code: int
    code: str
    msg_code: str
    msg: str
    detail: dict
    ex: Exception

    def __init__(
            self,
            *,
            status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
            code: str = "000000",
            msg_code: str = HTTPStatus.INTERNAL_SERVER_ERROR.description,
            msg: str = None,
            detail: dict = None,
            ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.msg_code = msg_code
        self.msg = msg
        self.detail = detail
        self.ex = ex
        super().__init__(ex)
