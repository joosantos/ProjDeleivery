from typing import Optional
from pydantic import UUID4, BaseModel
from .athlete import Athlete


class AthleteGroupBase(BaseModel):
    athlete_id: UUID4
    athlete_competition_id: UUID4


class AthleteGroupCreate(BaseModel):
    athlete_id: Optional[UUID4]
    athlete_competition_id: Optional[UUID4]


class AthleteGroupUpdate(BaseModel):
    athlete_id: Optional[UUID4]
    athlete_competition_id: Optional[UUID4]


class AthleteGroupInDBBase(AthleteGroupBase):
    athlete: Optional[Athlete] = None

    class Config:
        from_attributes = True


class AthleteGroup(AthleteGroupInDBBase):
    pass


class AthleteGroupInDB(AthleteGroupInDBBase):
    pass
