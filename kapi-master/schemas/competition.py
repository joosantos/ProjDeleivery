from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from .tournament import Tournament, TournamentInscriptionsNoMatches, TournamentNoMatches


class CompetitionBase(BaseModel):
    name: Optional[str] = None
    show_public: Optional[bool] = None
    calculate_age_start_year: Optional[bool] = None
    notes: Optional[str] = None


class CompetitionCreateUpdateBase(CompetitionBase):
    inscriptions_start: Optional[str] = None
    inscriptions_end: Optional[str] = None
    competition_start: Optional[str] = None
    competition_end: Optional[str] = None
    competition1: Optional[UUID4] = None
    competition2: Optional[UUID4] = None
    show_public: Optional[bool] = False
    from_other: Optional[bool] = False
    merge_unpair_tournaments: Optional[bool] = True
    create_empty_tournaments: Optional[bool] = True


# Properties to receive via API on creation
class CompetitionCreate(CompetitionCreateUpdateBase):
    pass


# Properties to receive via API on update
class CompetitionUpdate(CompetitionCreateUpdateBase):
    pass


class CompetitionInDBBase(CompetitionBase):
    id: UUID4
    inscriptions_start: Optional[datetime] = None
    inscriptions_end: Optional[datetime] = None
    competition_start: Optional[datetime] = None
    competition_end: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompetitionDetails(CompetitionInDBBase):
    tournaments: int
    matches: int
    athletes: int
    direct_winners: int


# Additional properties to return via API
class Competition(CompetitionInDBBase):
    tournaments: List[Tournament]


class CompetitionNoMatches(CompetitionInDBBase):
    tournaments: List[TournamentInscriptionsNoMatches]


class CompetitionNoMatchesNoInscriptions(CompetitionInDBBase):
    tournaments: List[TournamentNoMatches]


# Additional properties stored in DB
class CompetitionInDB(CompetitionInDBBase):
    pass
