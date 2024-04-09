from typing import Optional
from pydantic import UUID4, BaseModel
from .identification_document import IdentificationDocument


class PrivateInfoBase(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    nationality: Optional[str] = None
    natural_region: Optional[str] = None
    natural_country: Optional[str] = None
    gender_is_male: Optional[str] = None
    federation_number: int | None = None
    federation_active: Optional[bool] = None
    nif: Optional[str] = None


class PrivateInfoCreate(PrivateInfoBase):
    identification_document_id: Optional[UUID4] = None


class PrivateInfoUpdate(PrivateInfoBase):
    pass


class PrivateInfoInDBBase(PrivateInfoBase):
    id: UUID4
    identification_document_id: Optional[UUID4] = None
    identification_document: Optional[IdentificationDocument] = None

    class Config:
        from_attributes = True


class PrivateInfo(PrivateInfoInDBBase):
    pass


class PrivateInfoInDB(PrivateInfoInDBBase):
    pass
