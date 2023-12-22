from enum import Enum


class Language(str, Enum):
    ko: str = "ko"
    en: str = "en"


class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"
    apple: str = "apple"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class UserStatus(str, Enum):
    blocked: str = "blocked"
    deleted: str = "deleted"
    inactive: str = "inactive"
    active: str = "active"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))