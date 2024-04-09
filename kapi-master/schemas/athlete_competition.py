from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel
from .athlete_group import AthleteGroup


class AthleteCompetitionBase(BaseModel):
    competition_id: Optional[UUID4]


# Properties to receive via API on creation
class AthleteCompetitionCreate(AthleteCompetitionBase):
    pass


# Properties to receive via API on update
class AthleteCompetitionUpdate(AthleteCompetitionBase):
    pass


class AthleteCompetitionInDBBase(AthleteCompetitionBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# Additional properties to return via API
class AthleteCompetition(AthleteCompetitionInDBBase):
    athletes_group: List[AthleteGroup] = []


# Additional properties stored in DB
class AthleteCompetitionInDB(AthleteCompetitionInDBBase):
    pass
