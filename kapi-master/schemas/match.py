from datetime import datetime
from typing import List, Optional
from .athlete_competition import AthleteCompetition

from pydantic import UUID4, BaseModel


class MatchesTournamentCreate(BaseModel):
    ids: List[UUID4] = []


# Properties to receive via API on creation
class MatchCreate(BaseModel):
    tournament_id: Optional[UUID4] = None
    athlete_red_id: Optional[UUID4] = None
    athlete_blue_id: Optional[UUID4] = None
    number: Optional[int] = None


# Properties to receive via API on update
class MatchUpdate(MatchCreate):
    number_by_area: Optional[int] = None
    points_red_total: Optional[float] = None
    points_red_central_referee_round1: Optional[float] = None
    points_red_judge1_round1: Optional[float] = None
    points_red_judge2_round1: Optional[float] = None
    points_red_central_referee_round2: Optional[float] = None
    points_red_judge1_round2: Optional[float] = None
    points_red_judge2_round2: Optional[float] = None
    points_blue_total: Optional[float] = None
    points_blue_central_referee_round1: Optional[float] = None
    points_blue_judge1_round1: Optional[float] = None
    points_blue_judge2_round1: Optional[float] = None
    points_blue_central_referee_round2: Optional[float] = None
    points_blue_judge1_round2: Optional[float] = None
    points_blue_judge2_round2: Optional[float] = None
    winner_id: Optional[UUID4] = None
    normal_win: Optional[bool] = None
    abdicate_win: Optional[bool] = None
    no_show_win: Optional[bool] = None
    disqualified_win: Optional[bool] = None


class MatchRequestUpdate(BaseModel):
    area_to_call: Optional[str] = None
    description_to_micro: Optional[str] = None
    call_type: Optional[str] = None


class MatchRequestSpecial(BaseModel):
    call_request_fireman: Optional[bool] = None
    call_request_clean: Optional[bool] = None
    area_to_call: Optional[str] = None


class MatchInDBBase(MatchUpdate):
    id: UUID4
    athlete_red: Optional[AthleteCompetition] = None
    athlete_blue: Optional[AthleteCompetition] = None
    winner: Optional[AthleteCompetition] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# Additional properties to return via API
class Match(MatchInDBBase):
    pass


class MatchCalls(Match):
    call_request: Optional[bool] = None
    number_call_request: Optional[int] = None
    calls_made: Optional[int] = None
    area_to_call: Optional[str] = None
    description_to_micro: Optional[str] = None
    call_type: Optional[str] = None
    call_request_fireman: Optional[bool] = None
    call_request_clean: Optional[bool] = None


# Additional properties stored in DB
class MatchInDB(MatchInDBBase):
    pass
