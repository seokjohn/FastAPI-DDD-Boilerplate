from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import Query
from humps import camel


def to_camel(string):
    return camel.case(string)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class InfoModel(CamelModel):
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None


class Paginate(CamelModel):
    size: int = Field(0, nullable=False)
    total: int = Field(0, nullable=False)


class PaginateByPage(Paginate):
    page: int = Field(0, nullable=False)


class QueryParamSize(CamelModel):
    size: int = Query(10, example=10)


class QueryParamPage(CamelModel):
    page: int = Query(1, example=1)


class QueryParamPaginateByCursor(QueryParamSize):
    cursor: str = Query("", example="")


class CursorDirection(str, Enum):
    next: str = "next"
    prev: str = "prev"
    both: str = "both"


class QueryParamPaginateByTwoWayCursor(QueryParamPaginateByCursor):
    direction: CursorDirection = Query(CursorDirection.next, description="날짜 역순 기준")


class PaginateByTwoWayCursor(Paginate):
    prev_cursor: Optional[str] = Field("", nullable=False)
    next_cursor: Optional[str] = Field("", nullable=False)


class QueryParamPaginateByPage(QueryParamSize, QueryParamPage):
    ...

