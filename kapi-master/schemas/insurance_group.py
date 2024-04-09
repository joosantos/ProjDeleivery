from typing import Optional
from pydantic import UUID4, BaseModel
from datetime import datetime


class InsuranceGroupBase(BaseModel):
    name: str
    description: str


class InsuranceGroupCreate(InsuranceGroupBase):
    name: str
    description: str


class InsuranceGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class InsuranceGroupInDBBase(InsuranceGroupBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


class InsuranceGroup(InsuranceGroupInDBBase):
    pass


class InsuranceGroupInDB(InsuranceGroupInDBBase):
    pass
