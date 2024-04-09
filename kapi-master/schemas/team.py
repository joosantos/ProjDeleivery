from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel

from .user import User, UserAdminBase
from .insured_entity import InsuredEntity


class TeamName(BaseModel):
    id: UUID4
    name: str
    abbreviation: str


class TeamBase(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    association: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None


# Properties to receive via API on creation
class TeamCreate(TeamBase):
    coach_id: Optional[UUID4] = None
    insured_entity_id: Optional[str] = None


# Properties to receive via API on update
class TeamUpdate(TeamBase):
    insured_entity_id: Optional[str] = None
    notes: Optional[str] = None
    federation_number: int | None = None


class TeamInDBBase(TeamBase):
    id: Optional[UUID4]
    coach_id: Optional[UUID4] = None
    coach: Optional[User] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# Additional properties to return via API
class Team(TeamInDBBase):
    federated_in_current_season: bool = False


class TeamAdmin(Team):
    insured_entity_id: Optional[UUID4] = None
    insured_entity: Optional[InsuredEntity] = None
    notes: Optional[str] = None
    coach: Optional[UserAdminBase] = None
    federation_number: int | None = None


# Additional properties stored in DB
class TeamInDB(TeamAdmin):
    pass
