from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel


class IdentificationDocumentBase(BaseModel):
    type: Optional[str] = None
    number: Optional[str] = None
    emitted_by: Optional[str] = None


class IdentificationDocumentCreate(IdentificationDocumentBase):
    expiration_date: Optional[str] = None


class IdentificationDocumentUpdate(IdentificationDocumentBase):
    expiration_date: Optional[str] = None


class IdentificationDocumentInDBBase(IdentificationDocumentBase):
    id: UUID4
    expiration_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class IdentificationDocument(IdentificationDocumentInDBBase):
    pass


class IdentificationDocumentInDB(IdentificationDocumentInDBBase):
    pass
