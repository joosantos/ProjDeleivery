from datetime import datetime
from typing import Optional, List
from pydantic import UUID4, BaseModel
from .insurance import Insurance


class Insured(BaseModel):
    id: UUID4
    name: str

    class Config:
        from_attributes = True


class InsuredEntityBase(BaseModel):
    athlete_id: UUID4 | str | None = None
    team_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None


class InsuredEntityCreate(InsuredEntityBase):
    pass


class InsuredEntityUpdate(InsuredEntityBase):
    pass


class InsuredEntityInDBBase(InsuredEntityBase):
    id: UUID4
    insurances: List[Insurance] = []
    athlete_id: Optional[UUID4] = None
    team_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None
    athlete: Optional[Insured] = None
    team: Optional[Insured] = None
    user: Optional[Insured] = None

    class Config:
        from_attributes = True


class InsuredEntity(InsuredEntityInDBBase):
    pass


class InsuredEntityInDB(InsuredEntityInDBBase):
    pass
