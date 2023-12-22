from enum import Enum


class OrderBy(str, Enum):
    asc: str = "asc"
    desc: str = "desc"
