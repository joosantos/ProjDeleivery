from pydantic import UUID4, BaseModel


class PenalizationBase(BaseModel):
    description: str
    points: float
    competition_id: UUID4
    team_id: UUID4


# Properties to receive via API on creation
class PenalizationCreate(PenalizationBase):
    pass


# Properties to receive via API on update
class PenalizationUpdate(BaseModel):
    description: str | None = None
    points: float | None = None


class PenalizationInDBBase(PenalizationBase):
    id: UUID4

    class Config:
        from_attributes = True


class Penalization(PenalizationInDBBase):
    pass


# Additional properties stored in DB
class PenalizationInDB(Penalization):
    pass
