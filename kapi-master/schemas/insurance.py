from datetime import datetime
from typing import Optional, List
from pydantic import UUID4, BaseModel
from .insurance_group import InsuranceGroup
from .insurance_type import InsuranceType
from .private_info import PrivateInfo
from .geral_schemas import Date
from models import InsuranceStatusEnum


class Insured(BaseModel):
    id: UUID4
    name: str
    abbreviation: str | None = None
    profile_picture_url: str | None = None
    birthday: datetime | None = None
    private_info_id: UUID4 | None = None
    private_info: PrivateInfo | None = None

    class Config:
        from_attributes = True


class InsuredTeam(BaseModel):
    id: UUID4
    name: str
    abbreviation: str
    coach_id: UUID4 | str
    coach: Insured

    class Config:
        from_attributes = True


class Entity(BaseModel):
    id: UUID4
    athlete_id: Optional[UUID4] = None
    team_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None
    athlete: Optional[Insured] = None
    team: Optional[Insured] = None
    user: Optional[Insured] = None

    class Config:
        from_attributes = True


class InsuranceCreate(BaseModel):
    insurance_start_date: str
    insurance_end_date: str
    insurance_type_id: str
    insurance_group_id: Optional[str] = None
    federation_active: Optional[bool] = None


class InsuranceCreateMulti(BaseModel):
    start_date: Date
    insurance_type_id: str
    insurance_group_id: Optional[str] = None
    insured_entities_ids: List[str] = []
    sub_team_group: str


class InsuranceUpdateMulti(BaseModel):
    start_date: Date
    insurance_type_id: str
    insured_entities_ids: List[str] = []
    notes: str | None = None


class InsuranceUpdateMultiStatus(BaseModel):
    ids: list[UUID4]
    status: InsuranceStatusEnum
    notes: str | None = None


class InsuranceUpdateMultiGroups(BaseModel):
    ids: list[UUID4]
    insurance_group_id: UUID4 | None = None


class InsuranceCreateDatetime(BaseModel):
    start_date: datetime
    end_date: datetime
    insurance_type_id: str
    insurance_group_id: Optional[str] = None
    insured_entity_id: str
    sub_team_group: str
    status: str


class InsuranceUpdate(BaseModel):
    insurance_date: Optional[str] = None
    insurance_type_id: Optional[str] = None
    insurance_group_id: Optional[str] = None
    status: InsuranceStatusEnum | None = None
    notes: str | None = None


class InsuranceUpdateDatetime(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    insurance_type_id: Optional[str] = None
    insurance_group_id: Optional[str] = None
    medical_exam_url: Optional[str] = None
    payment_comprovative_url: Optional[str] = None
    contract_url: Optional[str] = None
    coach_certificate_url: Optional[str] = None
    status: Optional[str] = None
    sub_team_group: Optional[str] = None
    notes: str | None = None


class InsuranceInDBBase(BaseModel):
    id: UUID4
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[InsuranceStatusEnum] = None
    notes: str | None = None

    insured_entity_id: Optional[UUID4] = None
    insured_entity: Optional[Entity] = None

    insurance_type_id: Optional[UUID4] = None
    insurance_type: Optional[InsuranceType] = None

    insurance_group_id: Optional[UUID4] = None
    insurance_group: Optional[InsuranceGroup] = None

    sub_team_group: Optional[UUID4] = None
    medical_exam_url: Optional[str] = None
    payment_comprovative_url: Optional[str] = None
    contract_url: Optional[str] = None
    coach_certificate_url: Optional[str] = None

    class Config:
        from_attributes = True


class Insurance(InsuranceInDBBase):
    pass


class InsuranceTeamSubGroup(BaseModel):
    number_insured: int
    sub_team_group: str
    insurance_type_id: UUID4
    insurance_type: InsuranceType
    number_medical_exams: int
    number_payment_comprovatives: int
    number_pending: int
    number_accepted: int
    number_other_status: int
    profile_pictures: list[str]


class InsuranceGroupped(BaseModel):
    number_insured: int
    payment_comprovative_url: str | None = None
    contract_url: str | None = None
    coach_certificate_url: str | None = None
    insurance_group_id: UUID4 | None = None
    number_medical_exams: int
    number_payment_comprovatives: int
    number_pending: int
    number_accepted: int
    number_other_status: int
    profile_pictures: list[str]
    team_ids: list[str]
    teams: list[InsuredTeam]
    insurance_group_name: str


class InsuranceInDB(InsuranceInDBBase):
    pass


class InsurancePage(BaseModel):
    insurances: List[Insurance] = []
    skip: int
    limit: int
    total_elements: int
    total_pages: int
    current_page: int
