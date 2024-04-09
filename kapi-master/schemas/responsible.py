from typing import Optional
from pydantic import UUID4, BaseModel

from .identification_document import IdentificationDocument


class ResponsibleBase(BaseModel):
    name: Optional[str] = None
    relationship: Optional[str] = None
    email: Optional[str] = None


class ResponsibleCreate(ResponsibleBase):
    identification_document_id: Optional[UUID4] = None


class ResponsibleUpdate(ResponsibleBase):
    pass


class ResponsibleInDBBase(ResponsibleBase):
    id: UUID4
    identification_document_id: Optional[UUID4] = None
    identification_document: Optional[IdentificationDocument] = None

    class Config:
        from_attributes = True


class Responsible(ResponsibleInDBBase):
    pass


class ResponsibleInDB(ResponsibleInDBBase):
    pass
