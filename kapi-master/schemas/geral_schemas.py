from typing import Optional, Generic, TypeVar
from pydantic import UUID4, BaseModel
from datetime import datetime, date


class ListIds(BaseModel):
    ids: list[str]


class InscriptionPaymentIn(BaseModel):
    athlete_competition_id: UUID4
    tournament_id: UUID4


class Podium(BaseModel):
    first: Optional[UUID4] = None
    second: Optional[UUID4] = None
    third: Optional[UUID4] = None
    podium_notes: Optional[str] = None


result_type = TypeVar("result_type")


class PagedResponse(BaseModel, Generic[result_type]):
    results: list[result_type]
    n_results: int


class Date(date):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: date | str, validation_info) -> date:
        """
        Checks if the received value can be converted to a valid date and if
        so, returns it.
        """
        if isinstance(value, date):
            return value
        elif isinstance(value, str):
            return datetime.strptime(value, "%d-%m-%Y")
