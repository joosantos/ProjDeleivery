from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel

from .address import Address, AddressCreate
from .belt import Belt
from .category import Category
from .identification_document import (
    IdentificationDocumentCreate,
)
from .insured_entity import InsuredEntity
from .private_info import PrivateInfo, PrivateInfoCreate
from .responsible import Responsible, ResponsibleCreate
from .team import Team
from .user import UserAdminBase


class Tournament(BaseModel):
    is_male: Optional[bool] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    weight_min: Optional[int] = None
    weight_max: Optional[int] = None
    belt_min_id: Optional[UUID4] = None
    belt_max_id: Optional[UUID4] = None
    category_id: Optional[UUID4] = None
    competition_id: Optional[UUID4] = None
    competition_name: Optional[str] = None
    id: UUID4
    category: Optional[Category] = None
    belt_min: Optional[Belt] = None
    belt_max: Optional[Belt] = None

    class Config:
        from_attributes = True


class AthleteBase(BaseModel):
    name: Optional[str] = None
    is_male: Optional[bool] = None
    weight: Optional[float] = None
    is_adapted: Optional[bool] = None


class AthleteEditBase(AthleteBase):
    birthday: Optional[str] = None
    notes: Optional[str] = None
    team_id: Optional[str] = None
    belt_id: Optional[str] = None
    insured_entity_id: Optional[str] = None
    private_info_id: Optional[str] = None
    address_id: Optional[str] = None
    responsible_id: Optional[str] = None


# Properties to receive via API on creation
class AthleteCreate(AthleteEditBase):
    pass


# Properties to receive via API on update
class AthleteUpdate(AthleteEditBase):
    profile_picture_url: str | None = None


class AthleteInDBBase(AthleteBase):
    id: UUID4
    birthday: Optional[datetime] = None
    profile_picture_url: str | None = None

    team_id: Optional[UUID4] = None
    belt_id: Optional[UUID4] = None

    team: Optional[Team] = None
    belt: Optional[Belt] = None

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Athlete(AthleteInDBBase):
    federated_in_current_season: bool = False


class AthleteTournaments(Athlete):
    first: list[Tournament] = []
    second: list[Tournament] = []
    third: list[Tournament] = []
    other: list[Tournament] = []

    class Config:
        from_attributes = True


class AthletePrivate(Athlete):
    private_info_id: Optional[UUID4] = None
    address_id: Optional[UUID4] = None
    responsible_id: Optional[UUID4] = None
    insured_entity_id: Optional[UUID4] = None

    private_info: Optional[PrivateInfo] = None
    address: Optional[Address] = None
    responsible: Optional[Responsible] = None
    insured_entity: Optional[InsuredEntity] = None


class AthleteAdmin(AthletePrivate):
    user_id: UUID4 | None = None
    user: UserAdminBase | None = None
    notes: Optional[str] = None


# Additional properties stored in DB
class AthleteInDB(AthleteAdmin):
    pass


class AthleteCompleteCreate(BaseModel):
    public_data: AthleteCreate
    private_data: PrivateInfoCreate
    responsible: ResponsibleCreate
    address: AddressCreate
    identification: IdentificationDocumentCreate
    identification_responsible: IdentificationDocumentCreate
    notes: Optional[str] = None


class AthleteAdminUpdate(BaseModel):
    notes: Optional[str] = None


class AthletePrivatePage(BaseModel):
    athletes: List[AthletePrivate] = []
    skip: int
    limit: int
    total_elements: int
    total_pages: int
    current_page: int


class UserAdmin(UserAdminBase):
    athlete: AthleteAdmin | None = None
