from typing import Optional
from pydantic import UUID4, BaseModel


class BeltBase(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None


# Properties to receive via API on creation
class BeltCreate(BeltBase):
    pass


# Properties to receive via API on update
class BeltUpdate(BeltBase):
    pass


class BeltInDBBase(BeltBase):
    id: UUID4

    class Config:
        from_attributes = True


class Belt(BeltInDBBase):
    pass


# Additional properties stored in DB
class BeltInDB(Belt):
    pass
