from typing import Any, List, Dict
from copy import deepcopy
from core.exceptions import APIException, DEFALUT_STATUS_RESPONSE_INFO


class SetSwaggerException:
    def __init__(self, *args) -> None:
        self.defalut_status_info: Dict[Any, dict] = {}
        self.instances: List[APIException] = args

    def _serialize(self, inc: APIException) -> dict:
        return {inc.msg_code: {"summary": inc.msg_code,
                               "value": {"status": inc.status_code, "msg": inc.msg, "detail": inc.detail,
                                         "code": inc.code}}}

    def _set(self, code: int, values: dict):
        if self.defalut_status_info.get(code, None):
            self.defalut_status_info[code]["content"]["application/json"]["examples"].update(values)
        else:
            self.defalut_status_info[code] = deepcopy(DEFALUT_STATUS_RESPONSE_INFO[code])
            self.defalut_status_info[code]["content"]["application/json"]["examples"] = values

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        [self._set(inc().status_code, self._serialize(inc())) for inc in self.instances]
        return self.defalut_status_info


def set_swagger(*args) -> dict:
    return SetSwaggerException(*args)()
