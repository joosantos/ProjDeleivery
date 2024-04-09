from typing import Optional
from pydantic import UUID4, BaseModel


class InsuranceTypeBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fee: Optional[float] = None


class InsuranceTypeCreate(BaseModel):
    name: str
    description: str
    fee: float


class InsuranceTypeUpdate(InsuranceTypeBase):
    pass


class InsuranceTypeInDBBase(InsuranceTypeBase):
    id: UUID4

    class Config:
        from_attributes = True


class InsuranceType(InsuranceTypeInDBBase):
    pass


class InsuranceTypeInDB(InsuranceTypeInDBBase):
    pass
