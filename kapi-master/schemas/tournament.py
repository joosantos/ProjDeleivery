from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel
from .match import Match
from .category import Category
from .belt import Belt
from .athlete_competition import AthleteCompetition


class RefereesUpdate(BaseModel):
    central_referee: Optional[str] = None
    judge1: Optional[str] = None
    judge2: Optional[str] = None


class Inscription(BaseModel):
    tournament_id: UUID4
    athlete_competition_id: UUID4
    confirmed: Optional[bool] = None
    accepted: Optional[bool] = None
    athlete_competition: Optional[AthleteCompetition] = None

    class Config:
        from_attributes = True


class TournamentBase(BaseModel):
    is_male: Optional[bool] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    day: Optional[int] = None
    order: Optional[int] = None
    morning: Optional[bool] = None
    weight_min: Optional[int] = None
    weight_max: Optional[int] = None
    belt_min_id: Optional[UUID4] = None
    belt_max_id: Optional[UUID4] = None
    central_referee: Optional[str] = None
    judge1: Optional[str] = None
    judge2: Optional[str] = None
    area: Optional[str] = None
    first_place_id: Optional[UUID4] = None
    second_place_id: Optional[UUID4] = None
    third_place_id: Optional[UUID4] = None
    price: float | None = None


# Properties to receive via API on creation
class TournamentCreate(TournamentBase):
    category_id: Optional[UUID4] = None
    competition_id: Optional[UUID4] = None
    category: Optional[str] = None


# Properties to receive via API on update
class TournamentUpdate(TournamentBase):
    pass


class TournamentNoMatches(TournamentBase):
    id: UUID4
    competition_id: Optional[UUID4] = None
    category_id: Optional[UUID4] = None
    category: Optional[Category] = None
    first_place: Optional[AthleteCompetition] = None
    second_place: Optional[AthleteCompetition] = None
    third_place: Optional[AthleteCompetition] = None
    belt_min: Optional[Belt] = None
    belt_max: Optional[Belt] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    printed: Optional[bool] = None
    podium_notes: Optional[str] = None

    class Config:
        from_attributes = True


class TournamentInscriptionsNoMatches(TournamentNoMatches):
    inscriptions: List[Inscription]


class TournamentInDBBase(TournamentNoMatches):
    matches: List[Match]


# Additional properties to return via API
class Tournament(TournamentInDBBase):
    inscriptions: List[Inscription]


# Additional properties to return via API
class TournamentNoInscriptions(TournamentInDBBase):
    pass


# Additional properties stored in DB
class TournamentInDB(TournamentInDBBase):
    pass


class TournamentPage(BaseModel):
    tournaments: List[Tournament]
    limit: int
    total_elements: int


class TournamentName(BaseModel):
    id: UUID4
    is_male: Optional[bool] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    weight_min: Optional[int] = None
    weight_max: Optional[int] = None
    belt_min_id: Optional[UUID4] = None
    belt_max_id: Optional[UUID4] = None
    belt_min: Optional[Belt] = None
    belt_max: Optional[Belt] = None
    competition_id: Optional[UUID4] = None
    category_id: Optional[UUID4] = None
    category: Optional[Category] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
