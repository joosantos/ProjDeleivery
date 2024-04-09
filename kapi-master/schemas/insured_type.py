from typing import Optional
from pydantic import UUID4, BaseModel


class InsuredTypeBase(BaseModel):
    name: Optional[str] = None


class InsuredTypeCreate(InsuredTypeBase):
    pass


class InsuredTypeUpdate(InsuredTypeBase):
    pass


class InsuredTypeInDBBase(InsuredTypeBase):
    id: UUID4

    class Config:
        from_attributes = True


class InsuredType(InsuredTypeInDBBase):
    pass


class InsuredTypeInDB(InsuredTypeInDBBase):
    pass
