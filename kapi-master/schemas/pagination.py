from pydantic import BaseModel
from typing import Generic, TypeVar
from fastapi import Query


class PageQueries:
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of results to skip."),
        limit: int = Query(
            20, ge=-1, description="Maximum number of results per page."
        ),
    ):
        self.skip = skip
        self.limit = limit


result_type = TypeVar("result_type")


class PaginatedResponse(BaseModel, Generic[result_type]):
    total_elements_count: int
    elements: list[result_type]

    class config:
        arbitrary_type_allowed = True
